import os
import sys
import pika
import flask
import random
import json
import requests

from flask import request, jsonify
from pymongo import MongoClient

app = flask.Flask(__name__)
app.config["DEBUG"] = True

url = os.environ.get("CLOUDAMQP_URL")

if url is None:
    print("Invalid AMQP URL Specified!")
    exit()

queue_name = os.environ.get("VERIFICATION_INPUTS_QUEUE")

if queue_name is None:
    print("Invalid Verification Inputs Queue Specified!")
    exit()

email_requests_queue_name = os.environ.get("EMAIL_REQUESTS_QUEUE")

if email_requests_queue_name is None:
    print("Invalid Email Requests Queue Specified!")
    exit()

mongoDbConnectionUrl = os.environ.get("MONGO_CONNECTION_STRING")

if mongoDbConnectionUrl is None:
    print("Invalid Mongo DB Connection String Specified!")
    exit()

calculationServiceUrl = os.environ.get("CALCULATION_SERVICE_URL")

if calculationServiceUrl is None:
    print("Invalid Calculation Service URL Specified!")
    exit()


adminEmailAddress = os.environ.get("FROM_EMAIL_ADDRESS")

if adminEmailAddress is None:
    print("Invalid From Email Address Specified!")
    exit()


def prepare_message(request):
    if request is None:
        print("Invalid Request Specified for Preparation of the Message!")
        return

    verificationRequest = {
        "request": {
            "requestNumber": request["request"]["requestNumber"],
            "requestDate": request["request"]["requestDate"]
        },
        "personalDetail": {
            "firstName": request["personalDetail"]["firstName"],
            "middleName": request["personalDetail"]["middleName"],
            "lastName": request["personalDetail"]["lastName"],
            "age": request["personalDetail"]["age"],
            "gender": request["personalDetail"]["gender"],
            "dateOfBirth": request["personalDetail"]["dateOfBirth"],
            "nationality": request["personalDetail"]["nationality"],
            "PAN": request["personalDetail"]["PAN"],
            "residentAddress": request["personalDetail"]["residentAddress"]
        },
        "employmentDetail": request["employmentDetail"],
        "identificationDetail": request["identificationDetail"]
    }

    return verificationRequest


def send_message(request):
    if request is None:
        print("Invalid Request Specified!")
        return

    verificationRequest = prepare_message(request)
    verificationRequestJson = json.dumps(verificationRequest)

    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange='', routing_key=queue_name, body=verificationRequestJson)
    connection.close()

    print("Message Sent Successfully!")


def send_email_request_message(requestNumber, request):
    if request is None:
        print("Invalid Request Specified for Email Requests!")
        return

    toEmailAddress = request["personalDetail"]["residentAddress"]["email"]
    subject = "Credit Card Enrolment Request"
    body = f"We have received a credit card enrolment request, and your reference number for future communications {requestNumber}"
    isBodyHtml = False
    purpose = "Credit Card Enrolment"
    requestDate = request["request"]["requestDate"]
    message = {
        "request": {
            "requestNumber": requestNumber,
            "requestDate": requestDate,
            "purpose": "Application Invitation"
        },
        "emailDetail": {
            "from": adminEmailAddress,
            "to": toEmailAddress,
            "subject": subject,
            "body": body,
            "isBodyHtml": isBodyHtml
        }
    }

    emailMessageJson = json.dumps(message)

    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    channel.queue_declare(queue=email_requests_queue_name, durable=True)
    channel.basic_publish(
        exchange='', routing_key=email_requests_queue_name, body=emailMessageJson)
    connection.close()

    print("Email Message Sent Successfully!")


def add_database_record(request):
    if request is None:
        print("Invalid Request Specified!")
        exit()

    client = MongoClient(mongoDbConnectionUrl)
    db = client.creditcardservicesdb
    collection = db.creditcardservices
    collection.insert_one(request)

    client.close()

    print("Database Record Added Successfully!")


def prepare_calculation_service_request_message(request):
    calculationServiceRequest = {
        "request": {
            "requestNumber": request["request"]["requestNumber"],
            "requestDate": request["request"]["requestDate"],
            "cardCategory": request["request"]["requestNumber"],
            "internationalUseRequestAmount": request["request"]["internationalUseRequestAmount"],
            "cardType": request["request"]["cardType"]
        },
        "employmentDetail": {
            "employmentType": request["employmentDetail"]["employmentType"],
            "companyName": request["employmentDetail"]["companyName"],
            "designation": request["employmentDetail"]["designation"],
            "grossAnnualIncome": request["employmentDetail"]["grossAnnualIncome"],
            "otherIncome": request["employmentDetail"]["otherIncome"],
            "percentageOfLoanServicingGrossIncome": request["employmentDetail"]["percentageOfLoanServicingGrossIncome"],
            "incomeTaxProvided": request["employmentDetail"]["incomeTaxProvided"]
        },
        "bankRelationshipDetail": {
            "isExistingCustomer": request["bankRelationshipDetail"]["isExistingCustomer"],
            "accountNumber": request["bankRelationshipDetail"]["accountNumber"],
            "relationType": request["bankRelationshipDetail"]["relationType"]
        }
    }

    return calculationServiceRequest


def calculate_offer(request):
    print(request)
    calculationServiceRequest = \
        prepare_calculation_service_request_message(request)

    print(calculationServiceRequest)

    headers = {"Content-Type": "application/json"}

    response = requests.post(url=calculationServiceUrl, data=json.dumps(
        calculationServiceRequest), headers=headers)

    calculationOfferResponse = json.loads(response.content)

    return calculationOfferResponse


@app.route('/', methods=['GET'])
def home():
    return '<h1>Welcome to Credit Card Enrolment Services</h1>'


@app.route('/', methods=['POST'])
def process_record():
    record = json.loads(request.data)

    requestNumber = f"REQ-{random.randint(1000000, 10000000)}"
    requestDate = record["request"]["requestDate"]
    record["request"]["requestNumber"] = requestNumber
    record["request"]["status"] = "INITIATED"

    dbRecord = record.copy()

    calculationOfferRespones = calculate_offer(dbRecord)

    dbRecord["offerDetails"] = calculationOfferRespones["offerDetails"]

    add_database_record(dbRecord)
    send_message(record)
    send_email_request_message(requestNumber, record)

    response = {
        "requestNumber": requestNumber,
        "requestDate": requestDate
    }

    return jsonify(response)


app.run()
