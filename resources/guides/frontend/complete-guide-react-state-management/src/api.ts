import type { NewProduct, PaginatedProducts, Product } from "./types";

// In-memory stand-in for a REST API. Every call simulates latency so loading
// states, request dedup, and optimistic rollbacks are visible in the demo.

const latency = (ms = 300) =>
  new Promise<void>((resolve) => setTimeout(resolve, ms));

const seedProducts: Product[] = [
  {
    id: "prod-1",
    name: "Aurora Mechanical Keyboard",
    description: "Hot-swappable 75% board with tactile switches.",
    price: 129.99,
    category: "Peripherals",
  },
  {
    id: "prod-2",
    name: "Nimbus Headphones",
    description: "Over-ear ANC headphones with 40h battery.",
    price: 249,
    category: "Audio",
  },
  {
    id: "prod-3",
    name: "Drift Ergonomic Chair",
    description: "Mesh-back task chair with adjustable lumbar support.",
    price: 449.5,
    category: "Furniture",
  },
  {
    id: "prod-4",
    name: "Lumen Desk Lamp",
    description: "Dimmable LED lamp with a wireless charging base.",
    price: 59.99,
    category: "Lighting",
  },
  {
    id: "prod-5",
    name: "Vertex USB-C Hub",
    description: "7-in-1 hub: HDMI, SD, Ethernet, and 100W passthrough.",
    price: 79,
    category: "Peripherals",
  },
  {
    id: "prod-6",
    name: "Pulse Smart Bottle",
    description: "Insulated bottle that tracks hydration.",
    price: 34.95,
    category: "Drinkware",
  },
  {
    id: "prod-7",
    name: "Atlas Monitor Stand",
    description: "Gas-spring stand for ultrawide monitors.",
    price: 89,
    category: "Furniture",
  },
  {
    id: "prod-8",
    name: "Flux Desk Mat",
    description: "Stitched desk mat with a non-slip rubber base.",
    price: 39.5,
    category: "Accessories",
  },
];

let products = [...seedProducts];
let nextId = seedProducts.length + 1;

export const PRODUCTS_PAGE_SIZE = 3;

export async function fetchProducts(): Promise<Product[]> {
  await latency();
  return products.map((product) => ({ ...product }));
}

export async function fetchProductsPage(page = 1): Promise<PaginatedProducts> {
  await latency(400);
  const totalItems = products.length;
  const totalPages = Math.max(1, Math.ceil(totalItems / PRODUCTS_PAGE_SIZE));
  const safePage = Math.min(Math.max(1, page), totalPages);
  const start = (safePage - 1) * PRODUCTS_PAGE_SIZE;

  return {
    items: products
      .slice(start, start + PRODUCTS_PAGE_SIZE)
      .map((product) => ({ ...product })),
    page: safePage,
    pageSize: PRODUCTS_PAGE_SIZE,
    totalItems,
    totalPages,
    nextPage: safePage < totalPages ? safePage + 1 : null,
  };
}

export async function createProduct(
  input: NewProduct,
  options: { fail?: boolean } = {}
): Promise<Product> {
  await latency(500);
  if (options.fail) {
    throw new Error("Simulated server error — the product was not created");
  }
  const product: Product = { ...input, id: `prod-${nextId++}` };
  products = [...products, product];
  return { ...product };
}
