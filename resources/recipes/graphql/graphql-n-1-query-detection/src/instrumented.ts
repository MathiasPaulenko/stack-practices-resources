export interface QueryLog {
  count: number;
  queries: string[];
}

// Wraps any DB client in a Proxy that records every method call,
// including nested objects like db.users.findMany().
export function instrumentDbClient(db: any, queryLog: QueryLog) {
  const handler: ProxyHandler<any> = {
    get(target, prop) {
      const original = target[prop];
      if (typeof original === 'function') {
        return (...args: any[]) => {
          queryLog.count++;
          queryLog.queries.push(`${String(prop)}(${JSON.stringify(args[0] ?? {})})`);
          return original.apply(target, args);
        };
      }
      if (original && typeof original === 'object') {
        return new Proxy(original, handler);
      }
      return original;
    },
  };

  return new Proxy(db, handler);
}
