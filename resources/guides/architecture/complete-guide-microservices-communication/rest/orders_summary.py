from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

ORDER_SERVICE = "http://order-service:8000"
PAYMENT_SERVICE = "http://payment-service:8000"

@app.get("/orders/{order_id}/summary")
async def order_summary(order_id: str):
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            order = await client.get(f"{ORDER_SERVICE}/orders/{order_id}")
            order.raise_for_status()
            payment = await client.get(f"{PAYMENT_SERVICE}/payments/{order_id}")
            payment.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Upstream error: {e}")

    return {
        "order": order.json(),
        "payment": payment.json(),
    }
