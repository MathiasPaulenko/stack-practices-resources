// ProductGrid.tsx — pure presenter: no fetch, no store, only props in / UI out.
import React from 'react';

export interface Product {
  id: number;
  name: string;
  image: string;
  price: number;
}

export interface ProductGridProps {
  products: Product[];
  loading: boolean;
  error: string | null;
  onAddToCart: (productId: number) => void;
  layout?: 'grid' | 'list' | 'carousel';
}

export function ProductGrid({ products, loading, error, onAddToCart, layout = 'grid' }: ProductGridProps) {
  if (loading) return <div className="skeleton-grid">Loading products...</div>;
  if (error) return <div className="error-banner">{error}</div>;

  return (
    <div className={`product-${layout}`}>
      {products.map(product => (
        <div key={product.id} className="product-card">
          <img src={product.image} alt={product.name} />
          <h3>{product.name}</h3>
          <p className="price">${product.price}</p>
          <button onClick={() => onAddToCart(product.id)}>Add to Cart</button>
        </div>
      ))}
    </div>
  );
}
