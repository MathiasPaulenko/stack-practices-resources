export default function ProductsLoading() {
  return (
    <div className="mx-auto max-w-6xl space-y-4 p-6" aria-busy="true">
      <div className="h-8 w-40 animate-pulse rounded bg-zinc-200" />
      <div className="h-48 animate-pulse rounded-lg bg-zinc-200" />
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-3">
        {[0, 1, 2].map((i) => (
          <div key={i} className="h-72 animate-pulse rounded-lg bg-zinc-200" />
        ))}
      </div>
    </div>
  );
}
