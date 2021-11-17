using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace CalculationServiceAPI
{
    public class CalculationServiceRequestProcessor : ICalculationServiceRequestProcessor
    {
        private const string INVALID_REQUEST_DETAILS = "Invalid Calculation Request Details Specified!";
        public async Task<CalculationServiceResponse> Calculate(CalculationServiceRequest calculationServiceRequest)
        {
            var validation = calculationServiceRequest != default(CalculationServiceRequest) &&
                !string.IsNullOrEmpty(calculationServiceRequest.Request?.RequestNumber) &&
                !string.IsNullOrEmpty(calculationServiceRequest.Request?.CardType);

            if (!validation)
                throw new ApplicationException(INVALID_REQUEST_DETAILS);

            var response = await Task.Run<CalculationServiceResponse>(() => calculationServiceRequest.ApplyCalculations());

            response.AddRecordToDb();

            return response;
        }
    }
}
