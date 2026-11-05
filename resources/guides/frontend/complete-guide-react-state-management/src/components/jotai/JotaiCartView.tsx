import { useAtomValue, useSetAtom } from "jotai";
import {
  cartItemsAtom,
  cartTotalAtom,
  clearCartAtom,
  removeFromCartAtom,
  updateCartQuantityAtom,
} from "../../atoms/cartAtoms";
import { CartPanel } from "../CartPanel";

export function JotaiCartView() {
  const items = useAtomValue(cartItemsAtom);
  const total = useAtomValue(cartTotalAtom);
  const remove = useSetAtom(removeFromCartAtom);
  const update = useSetAtom(updateCartQuantityAtom);
  const clear = useSetAtom(clearCartAtom);

  return (
    <CartPanel
      items={items}
      total={total}
      onUpdateQuantity={(id, quantity) => update({ id, quantity })}
      onRemove={remove}
      onClear={clear}
    />
  );
}
