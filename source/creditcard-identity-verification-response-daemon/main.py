import pika
import sys
import os
import json
from pymongo import MongoClient

url = os.environ.get("CLOUDAMQP_URL")

if url is None:
    print("Invalid AMQP URL Specified!")
    exit()

mongoDbConnectionUrl = os.environ.get("MONGO_CONNECTION_STRING")

if mongoDbConnectionUrl is None:
    print("Invalid Mongo DB Connection String Specified!")
    exit()

queue_name = os.environ["VERIFICATION_RESPONSE_QUEUE"]

if queue_name is None:
    print('Invalid Verification Response Queue Name Specified!')
    exit()
        
def update_database(requestNumber, verificationResponse):
    print(f'Updating the database ... REQ # {requestNumber}')

    if requestNumber is None:
        print("Invalid Request Number Specified for Database Update!")
        exit()

    if verificationResponse is None:
        print("Invalid Verification Response Specified!")
        exit()


    client = MongoClient(mongoDbConnectionUrl)
    db = client.creditcardservicesdb
    collection = db.creditcardservices

    filter = {"request.requestNumber" : requestNumber}

    verificationStatus = {
        "personalDetailVerificationStatus": verificationResponse["personalDetailVerificationStatus"],
        "addressVerificationStatus": verificationResponse["addressVerificationStatus"],
        "employmentVerificationStatus": verificationResponse["employmentVerificationStatus"],
        "identificationDetailVerificationStatus": verificationResponse["identificationDetailVerificationStatus"],
        "messages": verificationResponse["messages"]
    }

    newElement = {"$set": {"verificationStatus": verificationStatus}}

    updateResult = collection.update_one(filter, newElement)

    if updateResult.modified_count == 1:
        print(f"{updateResult.modified_count} Row(s) Updated!")
    else:
        print("No / More Row(s) Affected!")

    client.close()


def process_message(body):
    verificationResponse = json.loads(body)
    requestNumber = verificationResponse["request"]["requestNumber"]

    print(f'Processing the Message ... REQ # {requestNumber}')

    update_database(requestNumber, verificationResponse)


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
