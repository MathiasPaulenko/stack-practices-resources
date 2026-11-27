export interface OrderItem {
  sku: string;
  quantity: number;
  priceCents: number;
}

export class Order {
  constructor(
    public id: string,
    public items: OrderItem[],
    public total: number,
    public customerEmail: string = ''
  ) {}
}
