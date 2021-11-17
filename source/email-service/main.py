import pika
import sys
import os
import json
import boto3
from pymongo import MongoClient

url = os.environ.get("CLOUDAMQP_URL")

if url is None:
    print("Invalid AMQP URL Specified!")
    exit()

ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")

if ACCESS_KEY is None:
    print("Invalid AWS Access Key Specified!")
    exit()

SECRET_KEY = os.environ.get("AWS_ACCESS_SECRET_KEY")

if SECRET_KEY is None:
    print("Invalid AWS Access Secret Key Specified!")
    exit()

REGION = os.environ.get("AWS_REGION")

if REGION is None:
    print("Invalid AWS Region Specified!")
    exit()


mongoDbConnectionUrl = os.environ.get("MONGO_CONNECTION_STRING")

if mongoDbConnectionUrl is None:
    print("Invalid Mongo DB Connection String Specified!")
    exit()

queue_name = os.environ["EMAIL_REQUESTS_QUEUE"]

if queue_name is None:
    print('Invalid Verification Response Queue Name Specified!')
    exit()


def send_email(name, source, subject, message, to):
    emailService = boto3.client("ses",
                                aws_access_key_id=ACCESS_KEY,
                                aws_secret_access_key=SECRET_KEY,
                                region_name=REGION)

    response = emailService.send_email(
        Destination={
            'ToAddresses': [to]
        },
        Message={
            'Body': {
                'Text': {
                    'Charset': 'UTF-8',
                    'Data': message
                },
            },
            'Subject': {
                'Charset': 'UTF-8',
                'Data': subject
            }
        },
        Source=source
    )

    return response


def add_database_record(requestNumber, emailRequest):
    print(f'Updating the database ... REQ # {requestNumber}')

    if requestNumber is None:
        print("Invalid Request Number Specified for Database Update!")
        exit()

    if emailRequest is None:
        print("Invalid Email Request Specified!")
        exit()

    client = MongoClient(mongoDbConnectionUrl)
    db = client.emailrequestsdb
    collection = db.emailrequests
    collection.insert_one(emailRequest)

    client.close()


def process_message(body):
    emailRequest = json.loads(body)
    requestNumber = emailRequest["request"]["requestNumber"]

    print(f'Processing the Message ... REQ # {requestNumber}')

    add_database_record(requestNumber, emailRequest)

    fromEmail = emailRequest["emailDetail"]["from"]
    to = emailRequest["emailDetail"]["to"]
    subject = emailRequest["emailDetail"]["subject"]
    body = emailRequest["emailDetail"]["body"]
    isBodyHtml = emailRequest["emailDetail"]["isBodyHtml"]

    send_email(name=fromEmail, source=fromEmail,
              subject=subject, message=body, to=to)


def main():
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)

    def callback(ch, method, properties, body):
        process_message(body)

    channel.basic_consume(
        queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
