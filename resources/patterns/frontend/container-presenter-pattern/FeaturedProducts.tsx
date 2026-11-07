// FeaturedProducts.tsx — container feeding the ProductGrid presenter.
import React, { useState, useEffect } from 'react';
import { ProductGrid, Product } from './ProductGrid';

export function FeaturedProducts() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/products?featured=true')
      .then(res => res.json())
      .then(data => { setProducts(data); setLoading(false); })
      .catch(err => { setError(err.message); setLoading(false); });
  }, []);

  const addToCart = (productId: number) => {
    fetch('/api/cart', {
      method: 'POST',
      body: JSON.stringify({ productId, quantity: 1 }),
    });
  };

  return (
    <section className="featured">
      <h2>Featured Products</h2>
      <ProductGrid
        products={products}
        loading={loading}
        error={error}
        onAddToCart={addToCart}
        layout="carousel"
      />
    </section>
  );
}
