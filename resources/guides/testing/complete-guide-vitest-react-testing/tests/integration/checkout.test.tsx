// tests/integration/checkout.test.tsx — Integration test
import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { CheckoutFlow } from "@/pages/CheckoutFlow";

vi.mock("@/api/orders", () => ({
  createOrder: vi.fn(),
  calculateShipping: vi.fn(),
}));

import { createOrder, calculateShipping } from "@/api/orders";

describe("Checkout flow integration", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(calculateShipping).mockResolvedValue({ cost: 5.99 });
    vi.mocked(createOrder).mockResolvedValue({ id: "order-123", status: "confirmed" });
  });

  it("completes full checkout flow", async () => {
    const user = userEvent.setup();
    render(<CheckoutFlow items={[{ id: 1, name: "Widget", price: 10, qty: 2 }]} />);

    // Step 1: Review cart
    expect(screen.getByText("Widget")).toBeInTheDocument();
    expect(screen.getByText("$20.00")).toBeInTheDocument();

    // Step 2: Enter shipping
    await user.click(screen.getByRole("button", { name: /continue to shipping/i }));
    await user.type(screen.getByLabelText(/address/i), "123 Main St");
    await user.type(screen.getByLabelText(/city/i), "New York");
    await user.type(screen.getByLabelText(/zip/i), "10001");

    // Wait for shipping calculation
    await waitFor(() => {
      expect(screen.getByText("$5.99")).toBeInTheDocument();
    });

    // Step 3: Place order
    await user.click(screen.getByRole("button", { name: /place order/i }));

    await waitFor(() => {
      expect(screen.getByText(/order confirmed/i)).toBeInTheDocument();
      expect(screen.getByText("order-123")).toBeInTheDocument();
    });

    expect(createOrder).toHaveBeenCalledWith(
      expect.objectContaining({
        items: expect.arrayContaining([
          expect.objectContaining({ id: 1, qty: 2 }),
        ]),
        shipping: expect.objectContaining({
          address: "123 Main St",
          city: "New York",
          zip: "10001",
        }),
      })
    );
  });
});
