import pika
import sys
import os
import json
import smtplib

from pymongo import MongoClient

url = os.environ.get("CLOUDAMQP_URL")

if url is None:
    print("Invalid AMQP URL Specified!")
    exit()

smtp_host = os.environ.get("SMTP_HOST")

if smtp_host is None:
    print("Invalid SMTP Host Specified!")
    exit()

smtp_port = os.environ.get("SMTP_PORT")

if smtp_port is None:
    print("Invalid SMTP Port Specified!")
    exit()

mongoDbConnectionUrl = os.environ.get("MONGO_CONNECTION_STRING")

if mongoDbConnectionUrl is None:
    print("Invalid Mongo DB Connection String Specified!")
    exit()

queue_name = os.environ["EMAIL_REQUESTS_QUEUE"]

if queue_name is None:
    print('Invalid Verification Response Queue Name Specified!')
    exit()


def send_email(source, subject, message, to):
    body = 'Subject: {}\n\n{}'.format(subject, message)

    try:
        smtpObj = smtplib.SMTP(smtp_host, smtp_port)
        smtpObj.sendmail(to, source, body)

        print("Mail has been sent successfully!")
    except smtplib.SMTPException as error:
        print("Error Occurred, Details : % s" % str(error))


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

    send_email(source=fromEmail,
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
