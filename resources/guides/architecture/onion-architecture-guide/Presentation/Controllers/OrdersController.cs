using Microsoft.AspNetCore.Mvc;
using OnionArchitecture.Application.Orders.PlaceOrder;

namespace OnionArchitecture.Presentation.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly PlaceOrderHandler _handler;

    public OrdersController(PlaceOrderHandler handler) => _handler = handler;

    [HttpPost]
    public async Task<IActionResult> Place([FromBody] PlaceOrderCommand command, CancellationToken ct)
    {
        var orderId = await _handler.Handle(command, ct);
        return CreatedAtAction(nameof(Place), new { id = orderId }, new { orderId });
    }
}
