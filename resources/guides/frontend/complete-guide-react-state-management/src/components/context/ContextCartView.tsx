import { useCart } from "../../context/CartContext";
import { CartPanel } from "../CartPanel";

export function ContextCartView() {
  const { state, dispatch } = useCart();

  return (
    <CartPanel
      items={state.items}
      total={state.total}
      onUpdateQuantity={(id, quantity) =>
        dispatch({ type: "UPDATE_QUANTITY", id, quantity })
      }
      onRemove={(id) => dispatch({ type: "REMOVE_ITEM", id })}
      onClear={() => dispatch({ type: "CLEAR" })}
    />
  );
}
