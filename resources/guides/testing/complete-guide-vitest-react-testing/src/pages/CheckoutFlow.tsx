import { useEffect, useState } from "react";
import { OrderItem, ShippingAddress, calculateShipping, createOrder } from "@/api/orders";

interface CheckoutFlowProps {
  items: OrderItem[];
}

type Step = "cart" | "shipping" | "done";

export function CheckoutFlow({ items }: CheckoutFlowProps) {
  const [step, setStep] = useState<Step>("cart");
  const [shipping, setShipping] = useState<ShippingAddress>({ address: "", city: "", zip: "" });
  const [shippingCost, setShippingCost] = useState<number | null>(null);
  const [orderId, setOrderId] = useState<string | null>(null);

  const subtotal = items.reduce((sum, i) => sum + i.price * i.qty, 0);

  useEffect(() => {
    if (step === "shipping") {
      calculateShipping(items).then((res) => setShippingCost(res.cost));
    }
  }, [step, items]);

  async function placeOrder() {
    const order = await createOrder({ items, shipping });
    setOrderId(order.id);
    setStep("done");
  }

  if (step === "done") {
    return (
      <section>
        <h2>Order confirmed</h2>
        <p>{orderId}</p>
      </section>
    );
  }

  if (step === "shipping") {
    return (
      <section>
        <h2>Shipping</h2>
        <label htmlFor="address">Address</label>
        <input
          id="address"
          value={shipping.address}
          onChange={(e) => setShipping({ ...shipping, address: e.target.value })}
        />
        <label htmlFor="city">City</label>
        <input
          id="city"
          value={shipping.city}
          onChange={(e) => setShipping({ ...shipping, city: e.target.value })}
        />
        <label htmlFor="zip">ZIP</label>
        <input
          id="zip"
          value={shipping.zip}
          onChange={(e) => setShipping({ ...shipping, zip: e.target.value })}
        />
        {shippingCost !== null && (
          <p>
            Shipping: <strong>${shippingCost.toFixed(2)}</strong>
          </p>
        )}
        <button onClick={placeOrder}>Place order</button>
      </section>
    );
  }

  return (
    <section>
      <h2>Your cart</h2>
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <span>{item.name}</span> — <span>${(item.price * item.qty).toFixed(2)}</span>
          </li>
        ))}
      </ul>
      <p>Total: ${subtotal.toFixed(2)}</p>
      <button onClick={() => setStep("shipping")}>Continue to shipping</button>
    </section>
  );
}
