namespace ECommerce.Application.Exceptions;

// Raised when a business rule blocks an operation. The controller maps
// it to 422; infrastructure exceptions map to 500 instead.
public class BusinessException : Exception
{
    public BusinessException(string message) : base(message) { }
}
