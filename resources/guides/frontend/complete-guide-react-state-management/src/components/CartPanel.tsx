import type { CartItem } from "../types";

interface CartPanelProps {
  items: CartItem[];
  total: number;
  onUpdateQuantity: (id: string, quantity: number) => void;
  onRemove: (id: string) => void;
  onClear: () => void;
}

// Presentational cart — each state approach wires its own state into this
// same markup so the comparison stays visual, not structural.
export function CartPanel({
  items,
  total,
  onUpdateQuantity,
  onRemove,
  onClear,
}: CartPanelProps) {
  return (
    <section className="cart-panel">
      <div className="section-head">
        <h2>Cart</h2>
        {items.length > 0 && (
          <button type="button" className="link" onClick={onClear}>
            Clear
          </button>
        )}
      </div>
      {items.length === 0 ? (
        <p className="muted">Cart is empty — add a product above.</p>
      ) : (
        <>
          <ul>
            {items.map((item) => (
              <li key={item.id} className="cart-item">
                <span className="cart-item-name">{item.name}</span>
                <span className="qty-controls">
                  <button
                    type="button"
                    aria-label={`Decrease quantity of ${item.name}`}
                    onClick={() => onUpdateQuantity(item.id, item.quantity - 1)}
                  >
                    −
                  </button>
                  <span>{item.quantity}</span>
                  <button
                    type="button"
                    aria-label={`Increase quantity of ${item.name}`}
                    onClick={() => onUpdateQuantity(item.id, item.quantity + 1)}
                  >
                    +
                  </button>
                </span>
                <span className="price">
                  ${(item.price * item.quantity).toFixed(2)}
                </span>
                <button
                  type="button"
                  className="link"
                  onClick={() => onRemove(item.id)}
                >
                  Remove
                </button>
              </li>
            ))}
          </ul>
          <p className="cart-total">
            Total: <strong>${total.toFixed(2)}</strong>
          </p>
        </>
      )}
    </section>
  );
}
