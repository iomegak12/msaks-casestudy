const mongodb = require("mongodb")
const amqplib = require('amqplib');

const MONGO_CONNECTION_STRING = process.env["MONGO_CONNECTION_STRING"]

if (!MONGO_CONNECTION_STRING) {
    console.error("Invalid Mongo DB Connection String Specified!");
    return;
}

const amqp_url = process.env["CLOUDAMQP_URL"];

if (!amqp_url) {
    console.log("Invalid AMQP URL for Response Message Specified!");
    return;
}

var responseQueue = process.env["RESPONSE_QUEUE"]

if (!responseQueue) {
    console.log("Invalid Response Queue Specified!");
    return;
}

var inputQueue = process.env["INPUT_QUEUE"];

if (!inputQueue) {
    console.log("Invalid Request Inputs Queue Specified!");
    return;
}

const saveRecordToDatabase = async record => {
    let client = null;

    try {
        client = await mongodb.connect(MONGO_CONNECTION_STRING, {
            useNewUrlParser: true,
            useUnifiedTopology: true
        });

        const database = client.db();
        const collection = database.collection("identityverificationrequests");

        if (collection) {
            const response = await collection.insertOne(record);

            if (response) {
                console.info("Record Processed Successfully!");
            } else {
                console.error("Unable to process the Record ... Try again!");
            }
        }
    } catch (error) {
        console.error(JSON.stringify(error));
    } finally {
        if (client) {
            await client.close(true);
        }
    }
};

const sendMessageToResponseQueue = async responseRecord => {
    var conn = await amqplib.connect(amqp_url, "heartbeat=60");
    var ch = await conn.createChannel()
    var exch = 'test_exchange';
    var rkey = 'test_route';
    var msg = JSON.stringify(responseRecord);

    await ch.assertExchange(exch, 'direct', { durable: true }).catch(console.error);
    await ch.assertQueue(responseQueue, { durable: true });
    await ch.bindQueue(responseQueue, exch, rkey);
    await ch.publish(exch, rkey, Buffer.from(msg));

    setTimeout(function () {
        ch.close();
        conn.close();

        console.log('Message Published Successfully!');
    }, 100);
};

const processRecord = async record => {
    if (!record) {
        console.log("Invalid Record Specified!");
        return;
    }

    const requestNumber = record.request.requestNumber;
    const nationality = record.personalDetail.nationality;
    const email = record.personalDetail.residentAddress.email;
    const phoneNumber = record.personalDetail.residentAddress.telephoneNumber;
    const employmentType = record.employmentDetail.employmentType;
    const grossAnnualIncome = parseInt(record.employmentDetail.grossAnnualIncome);
    const otherIncome = parseInt(record.employmentDetail.otherIncome);
    const incomeTaxProvided = record.employmentDetail.incomeTaxProvided;
    const identityType = record.identificationDetail.identityType;
    const identificationNumber = record.identificationDetail.identificationNumber;
    const percentageOfLoanServicingGrossIncome = parseInt(record.employmentDetail.percentageOfLoanServicingGrossIncome);

    const totalIncome = grossAnnualIncome + otherIncome;
    const totalIncomeAfterLoanPayments = parseInt(totalIncome * percentageOfLoanServicingGrossIncome * 0.01);
    const incomeVerificationStatus = incomeTaxProvided && totalIncomeAfterLoanPayments >= 1;

    const personalDetailVerificationStatus = nationality === "INDIAN";
    const addressVerificationStatus = email !== null && email !== "" && phoneNumber !== null &&
        phoneNumber !== "" && email !== undefined && phoneNumber !== undefined;
    const employmentVerificationStatus = employmentType === "SALARIED" && incomeVerificationStatus;
    const identityVerificationStatus = (identityType === "PASSPORT" ||
        identityType === "DRIVING LICENSE" || identityType === "VOTER ID" ||
        identityType === "PAN" || identityType === "GOVERNMENT ID") && identificationNumber !== null;

    const dbRequestRecord = {
        request: record.request,
        personalDetail: record.personalDetail,
        employmentDetail: record.employmentDetail,
        identificationDetail: record.identificationDetail,
        verificationDetails: {
            personalDetailVerificationStatus,
            addressVerificationStatus,
            employmentVerificationStatus,
            identityVerificationStatus
        }
    };

    await saveRecordToDatabase(dbRequestRecord);

    const messages = [];

    if (!personalDetailVerificationStatus) {
        messages.push("Invalid Nationality Specified!");
    }

    if (!addressVerificationStatus) {
        messages.push("Either Invalid Email or Phone Number Specified!");
    }

    if (!employmentVerificationStatus) {
        messages.push("Invalid Employment Type Specified (ONLY SALARIED), Insufficient Income Specified!");
    }

    if (!identityVerificationStatus) {
        messages.push("Invalid Identity Detail Specifid!");
    }

    const response = {
        request: {
            requestNumber: requestNumber
        },
        personalDetailVerificationStatus,
        addressVerificationStatus,
        employmentVerificationStatus,
        identificationDetailVerificationStatus: identityVerificationStatus,
        messages
    };

    await sendMessageToResponseQueue(response);
};

const processIncomingMessages = () => {
    var amqp = require('amqplib/callback_api');

    amqp.connect(amqp_url, function (error0, connection) {
        if (error0) {
            throw error0;
        }

        connection.createChannel(function (error1, channel) {
            if (error1) {
                throw error1;
            }

            var queue = inputQueue;

            channel.assertQueue(queue, {
                durable: true
            });

            console.log(" [*] Waiting for messages in %s. To exit press CTRL+C", queue);

            channel.consume(queue, function (msg) {
                channel.ack(msg);

                let incomingRequestRecord = JSON.parse(msg.content.toString());

                processRecord(incomingRequestRecord)
                    .then(() => console.log("Message Processing Completed"));
            }, {
                noAck: false
            });
        });
    });
};

processIncomingMessages();