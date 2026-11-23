function CartActions({ item }) {
  const [quantity, setQuantity] = useState(item.quantity);

  const updateQuantity = async (newQty) => {
    if (newQty === 0) {
      // Pessimistic — deleting from cart needs confirmation
      const confirmed = window.confirm('Remove this item from cart?');
      if (!confirmed) return;

      await fetch(`/api/cart/${item.id}`, { method: 'DELETE' });
      setQuantity(0);
    } else {
      // Optimistic — quantity change is low-risk
      const prev = quantity;
      setQuantity(newQty);
      try {
        await fetch(`/api/cart/${item.id}`, {
          method: 'PATCH',
          body: JSON.stringify({ quantity: newQty }),
        });
      } catch {
        setQuantity(prev);
      }
    }
  };

  return (
    <div>
      <button onClick={() => updateQuantity(quantity - 1)}>-</button>
      <span>{quantity}</span>
      <button onClick={() => updateQuantity(quantity + 1)}>+</button>
    </div>
  );
}
