const lazyPages: Record<string, () => Promise<unknown>> = {
  '/reports': () => import('../pages/Reports'),
  '/analytics': () => import('../pages/Analytics'),
};

export function prefetchRoute(path: string): void {
  lazyPages[path]?.();
}
