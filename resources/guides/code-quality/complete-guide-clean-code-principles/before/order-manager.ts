// BEFORE — everything wrong in one file. Refactor exercise:
// find the smells (naming, size, side effects, magic numbers, null)
// before looking at after/order-processor.ts

export class OrderManager {
  process(o: any): number {
    // validate
    if (!o.items || o.items.length === 0) {
      return -1; // error code: caller must check
    }
    // calculate
    let t = 0;
    for (let i = 0; i < o.items.length; i++) {
      const it = o.items[i];
      if (it.cat === 'food') t += it.p * 0.05;
      else if (it.cat === 'elec') t += it.p * 0.18;
      else t += it.p * 0.1;
    }
    // discount
    if (o.c.vip === true) {
      o.total = o.total * 0.9; // mutates the argument — hidden side effect
    }
    // save
    this.db.query('INSERT INTO orders VALUES (?, ?)', o.id, o.total);
    // email
    this.smtp.send(o.c.email, 'Order confirmed');
    return 1;
  }

  private db: any;
  private smtp: any;
}
