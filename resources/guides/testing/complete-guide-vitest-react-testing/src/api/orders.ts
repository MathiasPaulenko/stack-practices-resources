export interface OrderItem {
  id: number;
  name: string;
  price: number;
  qty: number;
}

export interface ShippingAddress {
  address: string;
  city: string;
  zip: string;
}

export interface Order {
  id: string;
  status: string;
}

export async function calculateShipping(items: OrderItem[]): Promise<{ cost: number }> {
  const res = await fetch(`${window.location.origin}/api/shipping`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ items }),
  });
  return res.json();
}

export async function createOrder(payload: {
  items: OrderItem[];
  shipping: ShippingAddress;
}): Promise<Order> {
  const res = await fetch(`${window.location.origin}/api/orders`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return res.json();
}
