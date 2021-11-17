using System;
using System.Collections.Generic;
using System.Text;
using System.Text.Json.Serialization;

namespace CalculationServiceAPI
{
    public class Request
    {
        [JsonPropertyName("requestNumber")]
        public string RequestNumber { get; set; }

        [JsonPropertyName("requestDate")]
        public string RequestDate { get; set; }

        [JsonPropertyName("cardCategory")]
        public string CardCategory { get; set; }

        [JsonPropertyName("internationalUseRequestAmount")]
        public int InternationalUseRequestAmount { get; set; }

        [JsonPropertyName("cardType")]
        public string CardType { get; set; }
    }

    public class EmploymentDetail
    {
        [JsonPropertyName("employmentType")]
        public string EmploymentType { get; set; }

        [JsonPropertyName("companyName")]
        public string CompanyName { get; set; }

        [JsonPropertyName("designation")]
        public string Designation { get; set; }

        [JsonPropertyName("grossAnnualIncome")]
        public int GrossAnnualIncome { get; set; }

        [JsonPropertyName("otherIncome")]
        public int OtherIncome { get; set; }

        [JsonPropertyName("percentageOfLoanServicingGrossIncome")]
        public int PercentageOfLoanServicingGrossIncome { get; set; }

        [JsonPropertyName("incomeTaxProvided")]
        public bool IncomeTaxProvided { get; set; }
    }

    public class BankRelationshipDetail
    {
        [JsonPropertyName("isExistingCustomer")]
        public bool IsExistingCustomer { get; set; }

        [JsonPropertyName("accountNumber")]
        public string AccountNumber { get; set; }

        [JsonPropertyName("relationType")]
        public string RelationType { get; set; }
    }

    public class CalculationServiceRequest
    {
        [JsonPropertyName("request")]
        public Request Request { get; set; }

        [JsonPropertyName("employmentDetail")]
        public EmploymentDetail EmploymentDetail { get; set; }

        [JsonPropertyName("bankRelationshipDetail")]
        public BankRelationshipDetail BankRelationshipDetail { get; set; }
    }


}
