using System;
using System.Collections.Generic;
using System.Text;

namespace CalculationServiceAPI
{
    public static class CalculationServiceLogic
    {
        public static CalculationServiceResponse ApplyCalculations(
            this CalculationServiceRequest calculationServiceRequest)
        {
            var response = calculationServiceRequest.Map();
            var random = new Random();

            response.OfferDetails.AddonCardFee = random.Next(100, 200);
            response.OfferDetails.AnnualFee = random.Next(500, 1000);
            response.OfferDetails.ChequeReturnFee = random.Next(100, 200);
            response.OfferDetails.CreditLimit = random.Next(100000, 500000);
            response.OfferDetails.ForeignCurrencyTransactionFee = random.Next(100, 500);
            response.OfferDetails.IssuingCharges = 0;
            response.OfferDetails.LatePaymentFee = 0;
            response.OfferDetails.PetrolTransactionCharges = random.Next(10, 50);
            response.OfferDetails.RailwayTicketPurchaseFee = random.Next(100, 200);
            response.OfferDetails.RateOfInterest = random.Next(12, 18);
            response.OfferDetails.RenewalFee = 0;
            response.OfferDetails.ReplacementOfLostCard = 0;

            return response;
        }
    }
}
