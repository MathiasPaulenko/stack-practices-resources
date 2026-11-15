import { useEffect, useRef } from 'react';
import { useInfiniteQuery } from '@tanstack/react-query';

// Data lazy loading: fetch one page, pull the next slice on demand.
// The sentinel div + IntersectionObserver turns "load more" into
// infinite scroll — the mechanics are identical to lazy images.
export default function ProductList() {
  const sentinelRef = useRef(null);
  const { data, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useInfiniteQuery({
      queryKey: ['products'],
      queryFn: ({ pageParam }) =>
        fetch(`/api/products?after=${pageParam ?? ''}`).then((r) => r.json()),
      initialPageParam: null,
      // Cursor-based pagination: stable when rows are inserted between fetches.
      getNextPageParam: (lastPage) => lastPage.nextCursor ?? undefined,
    });

  useEffect(() => {
    const sentinel = sentinelRef.current;
    if (!sentinel || !hasNextPage) return;

    const observer = new IntersectionObserver(
      (entries) => {
        if (entries[0].isIntersecting && !isFetchingNextPage) fetchNextPage();
      },
      { rootMargin: '300px 0px' }
    );
    observer.observe(sentinel);
    return () => observer.disconnect();
  }, [hasNextPage, isFetchingNextPage, fetchNextPage]);

  return (
    <>
      {data?.pages.map((page) =>
        page.products.map((p) => <ProductCard key={p.id} product={p} />)
      )}
      <div ref={sentinelRef} />
      {isFetchingNextPage && <p>Loading more…</p>}
      {!hasNextPage && data && <p>No more products.</p>}
    </>
  );
}
