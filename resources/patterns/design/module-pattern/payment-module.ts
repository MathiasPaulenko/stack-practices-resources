// PaymentModule — Module Pattern with lifecycle and enforced private state
// The IIFE variant still useful for singleton-style modules with state.

interface Transaction {
  id: string;
  amount: number;
  currency: string;
  status: "pending" | "completed" | "failed";
}

const PaymentModule = (function () {
  // Private: not accessible from outside
  let apiKey = "";
  const transactions: Transaction[] = [];
  const MAX_TRANSACTIONS = 1000;

  function validateKey(key: string): boolean {
    return key.startsWith("pk_") && key.length === 32;
  }

  function log(msg: string) {
    console.log(`[PAYMENT] ${new Date().toISOString()} ${msg}`);
  }

  // Public: exposed API
  return {
    init(key: string) {
      if (!validateKey(key)) throw new Error("Invalid API key");
      apiKey = key;
      log("Module initialized");
    },
    charge(amount: number, currency: string): Promise<Transaction> {
      if (!apiKey) throw new Error("Module not initialized");
      if (transactions.length >= MAX_TRANSACTIONS) {
        throw new Error("Transaction limit reached");
      }
      log(`Charging ${amount} ${currency}`);
      const tx: Transaction = {
        id: crypto.randomUUID(),
        amount,
        currency,
        status: "pending",
      };
      transactions.push(tx);
      return Promise.resolve(tx);
    },
    getTransactions(): Transaction[] {
      return [...transactions];
    },
    getStats() {
      return {
        total: transactions.length,
        pending: transactions.filter((t) => t.status === "pending").length,
        completed: transactions.filter((t) => t.status === "completed").length,
      };
    },
  };
})();

// Usage
PaymentModule.init("pk_test_1234567890123456789012345678");
await PaymentModule.charge(99.99, "USD");
console.log(PaymentModule.getStats()); // { total: 1, pending: 1, completed: 0 }
// PaymentModule.apiKey -> undefined (private)
// PaymentModule.validateKey -> undefined (private)
