import { useShallow } from "zustand/react/shallow";
import { useCartStore } from "../../stores/useCartStore";
import { CartPanel } from "../CartPanel";

export function ZustandCartView() {
  // An object selector returns a fresh reference on every call, so it needs
  // useShallow — otherwise the component re-renders on every store update.
  const { items, total, updateQuantity, removeItem, clear } = useCartStore(
    useShallow((s) => ({
      items: s.items,
      total: s.total,
      updateQuantity: s.updateQuantity,
      removeItem: s.removeItem,
      clear: s.clear,
    }))
  );

  return (
    <CartPanel
      items={items}
      total={total}
      onUpdateQuantity={updateQuantity}
      onRemove={removeItem}
      onClear={clear}
    />
  );
}
