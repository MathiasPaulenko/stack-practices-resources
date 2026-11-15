using ECommerce.Application.Dtos;
using ECommerce.Application.Exceptions;
using ECommerce.Application.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace ECommerce.Presentation.Controllers;

// Thin controller: translates HTTP, calls the service, formats the response.
// No DbContext, no business ifs — those live in Application/Domain.
[ApiController]
[Route("api/[controller]")]
public class OrderController : ControllerBase
{
    private readonly IOrderService _orderService;

    public OrderController(IOrderService orderService) =>
        _orderService = orderService;

    public record CreateOrderRequest(int ProductId, int Quantity);

    [HttpPost]
    public async Task<ActionResult<OrderDto>> Create(CreateOrderRequest request)
    {
        try
        {
            var dto = await _orderService.CreateOrderAsync(request.ProductId, request.Quantity);
            return CreatedAtAction(nameof(Get), new { id = dto.Id }, dto);
        }
        catch (BusinessException ex)
        {
            return UnprocessableEntity(new { error = ex.Message });
        }
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<OrderDto>> Get(int id)
    {
        var dto = await _orderService.GetOrderAsync(id);
        return dto is null ? NotFound() : Ok(dto);
    }
}
