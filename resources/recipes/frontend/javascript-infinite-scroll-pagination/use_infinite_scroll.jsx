// React hook: synchronous ref guard prevents double fetches when two
// intersection events land in the same tick before state updates.
import { useEffect, useRef, useState, useCallback } from "react";

export function useInfiniteScroll(fetchUrl) {
    const [items, setItems] = useState([]);
    const [page, setPage] = useState(1);
    const [loading, setLoading] = useState(false);
    const [hasMore, setHasMore] = useState(true);
    const sentinelRef = useRef(null);
    const loadingRef = useRef(false);

    const loadMore = useCallback(async () => {
        if (loadingRef.current) return;
        loadingRef.current = true;
        setLoading(true);

        try {
            const res = await fetch(`${fetchUrl}?page=${page}`);
            const data = await res.json();
            setItems(prev => [...prev, ...data.items]);
            setHasMore(data.hasMore);
            setPage(prev => prev + 1);
        } catch (err) {
            console.error("Failed to load:", err);
        } finally {
            loadingRef.current = false;
            setLoading(false);
        }
    }, [fetchUrl, page]);

    useEffect(() => {
        const sentinel = sentinelRef.current;
        if (!sentinel || !hasMore) return;

        const observer = new IntersectionObserver(
            (entries) => {
                if (entries[0].isIntersecting) loadMore();
            },
            { rootMargin: "300px" }
        );

        observer.observe(sentinel);
        return () => observer.disconnect();
    }, [loadMore, hasMore]);

    return { items, loading, hasMore, sentinelRef };
}
