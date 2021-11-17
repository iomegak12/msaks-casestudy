using System;
using System.Collections.Generic;
using System.Text;

namespace CalculationServiceAPI
{
    public static class CalculationServiceRequestToResponseMap
    {
        public static CalculationServiceResponse Map(this CalculationServiceRequest calculationServiceRequest)
        {
            var response = new CalculationServiceResponse
            {
                Request = calculationServiceRequest.Request,
                OfferDetails = new OfferDetails
                {
                    AddonCardFee = 0,
                    AnnualFee = 0,
                    ChequeReturnFee = 0,
                    CreditLimit = 0,
                    ForeignCurrencyTransactionFee = 0,
                    IssuingCharges = 0,
                    LatePaymentFee = 0,
                    PetrolTransactionCharges = 0,
                    RailwayTicketPurchaseFee = 0,
                    RateOfInterest = 0,
                    RenewalFee = 0,
                    ReplacementOfLostCard = 0
                }
            };

            return response;
        }
    }
}
