// Domain service: logic that doesn't naturally live inside one aggregate.
// Stateless, named in the ubiquitous language, free of persistence details.
import { Money } from "./money";

interface OrderItem {
  productId: string;
  quantity: number;
}

interface Product {
  id: string;
  category: string;
  price: Money;
}

interface Discount {
  percentage: number;
}

interface ProductRepository {
  findById(id: string): Product | undefined;
}

interface DiscountRepository {
  findActiveDiscount(customerId: string, category: string): Discount | undefined;
}

export class PricingService {
  constructor(
    private productRepo: ProductRepository,
    private discountRepo: DiscountRepository
  ) {}

  calculateTotal(items: OrderItem[], customerId: string): Money {
    let total = Money.zero("USD");

    for (const item of items) {
      const product = this.productRepo.findById(item.productId);
      if (!product) throw new Error(`Product ${item.productId} not found`);

      const basePrice = product.price.multiply(item.quantity);
      const discount = this.discountRepo.findActiveDiscount(
        customerId,
        product.category
      );

      const finalPrice = discount
        ? basePrice.subtract(basePrice.multiply(discount.percentage))
        : basePrice;

      total = total.add(finalPrice);
    }

    return total;
  }
}
