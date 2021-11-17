using System.Threading.Tasks;

namespace CalculationServiceAPI
{
    public interface ICalculationServiceRequestProcessor
    {
        Task<CalculationServiceResponse> Calculate(CalculationServiceRequest calculationServiceRequest);
    }
}