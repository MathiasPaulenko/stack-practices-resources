export type Theme = "light" | "dark";

export interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  category: string;
}

export type NewProduct = Omit<Product, "id">;

export interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

// What callers pass when adding to the cart — identity and pricing only.
// Extra Product fields (description, category) never leak into cart state.
export type CartItemInput = Omit<CartItem, "quantity">;

export interface PaginatedProducts {
  items: Product[];
  page: number;
  pageSize: number;
  totalItems: number;
  totalPages: number;
  nextPage: number | null;
}
