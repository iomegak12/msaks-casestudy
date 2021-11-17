using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

namespace CalculationServiceAPI
{
    public class OfferDetails
    {
        [JsonPropertyName("rateOfInterest")]
        public double RateOfInterest { get; set; }

        [JsonPropertyName("creditLimit")]
        public int CreditLimit { get; set; }

        [JsonPropertyName("petrolTransactionCharges")]
        public int PetrolTransactionCharges { get; set; }

        [JsonPropertyName("railwayTicketPurchaseFee")]
        public int RailwayTicketPurchaseFee { get; set; }

        [JsonPropertyName("foreignCurrencyTransactionFee")]
        public int ForeignCurrencyTransactionFee { get; set; }

        [JsonPropertyName("addonCardFee")]
        public int AddonCardFee { get; set; }

        [JsonPropertyName("renewalFee")]
        public int RenewalFee { get; set; }

        [JsonPropertyName("annualFee")]
        public int AnnualFee { get; set; }

        [JsonPropertyName("replacementOfLostCard")]
        public int ReplacementOfLostCard { get; set; }

        [JsonPropertyName("issuingCharges")]
        public int IssuingCharges { get; set; }

        [JsonPropertyName("latePaymentFee")]
        public int LatePaymentFee { get; set; }

        [JsonPropertyName("chequeReturnFee")]
        public int ChequeReturnFee { get; set; }
    }

    public class CalculationServiceResponse
    {
        [JsonPropertyName("request")]
        public Request Request { get; set; }

        [JsonPropertyName("offerDetails")]
        public OfferDetails OfferDetails { get; set; }
    }


}
