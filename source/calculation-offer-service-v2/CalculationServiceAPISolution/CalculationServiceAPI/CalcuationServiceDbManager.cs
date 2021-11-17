using MongoDB.Bson;
using MongoDB.Driver;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace CalculationServiceAPI
{
    public static class CalcuationServiceDbManager
    {
        private const string MONGO_CONNECTION_STRING = "MONGO_CONNECTION_STRING";
        private const string DATABASE_NAME = "calculationServiceRequestsDb";
        private const string COLLECTION_NAME = "calculationservicerequests";
        public static void AddRecordToDb(this CalculationServiceResponse calculationServiceResponse)
        {
            var connectionString = Environment.GetEnvironmentVariable(MONGO_CONNECTION_STRING);

            if (string.IsNullOrEmpty(connectionString))
                throw new ApplicationException("Invalid Mongo DB Connection String Specified!");

            var client = new MongoClient(connectionString);
            var database = client.GetDatabase(DATABASE_NAME);
            var collection = database.GetCollection<BsonDocument>(COLLECTION_NAME);
            var jsonString = JsonConvert.SerializeObject(calculationServiceResponse);
            var bsonDocument = BsonDocument.Parse(jsonString);

            collection.InsertOne(bsonDocument);
        }
    }
}
