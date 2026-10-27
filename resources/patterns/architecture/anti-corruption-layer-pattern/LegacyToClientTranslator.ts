// Legacy shape — what USR_MAST actually returns
interface LegacyCustAcct {
  CUST_ID: string;
  ACCT_NM: string;
  CR_LMT_AMT: number;
  ACCT_STAT_CD: 'A' | 'S' | 'C';
}

// Domain shape — what your code actually works with
interface Client {
  id: string;
  name: string;
  creditLimit: Money;
  status: 'active' | 'suspended' | 'closed';
}

class LegacyToClientTranslator {
  toDomain(legacy: LegacyCustAcct): Client {
    return {
      id: legacy.CUST_ID,
      name: legacy.ACCT_NM,
      creditLimit: { amount: legacy.CR_LMT_AMT, currency: 'USD' },
      status: { A: 'active', S: 'suspended', C: 'closed' }[legacy.ACCT_STAT_CD],
    };
  }
}
