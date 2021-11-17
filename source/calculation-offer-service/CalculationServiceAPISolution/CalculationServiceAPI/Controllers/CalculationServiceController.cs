using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace CalculationServiceAPI.Controllers
{
    [Route("api/calculation-services")]
    [ApiController]
    public class CalculationServiceController : ControllerBase
    {
        private ICalculationServiceRequestProcessor calculationServiceRequestProcessor = default(ICalculationServiceRequestProcessor);

        public CalculationServiceController(ICalculationServiceRequestProcessor calculationServiceRequestProcessor)
        {
            if (calculationServiceRequestProcessor == default(ICalculationServiceRequestProcessor))
                throw new ApplicationException("Invalid Calculation Service Request Processor Specified!");

            this.calculationServiceRequestProcessor = calculationServiceRequestProcessor;
        }

        [HttpPost("process")]
        public async Task<CalculationServiceResponse> Process(
            [FromBody] CalculationServiceRequest calculationServiceRequest)
        {
            var response = await calculationServiceRequestProcessor.Calculate(calculationServiceRequest);

            return response;
        }
    }
}
