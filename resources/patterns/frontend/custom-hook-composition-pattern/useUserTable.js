import { useMemo } from 'react';
import { useDebounce } from './useDebounce.js';
import { useFetch } from './useFetch.js';
import { useSort } from './useSort.js';
import { usePagination } from './usePagination.js';

/**
 * Composed hook: debounce -> url -> fetch -> sort -> paginate.
 * Data flows top-down; each hook consumes the previous output.
 */
export function useUserTable(searchQuery, options = {}) {
  const debouncedQuery = useDebounce(searchQuery, options.debounceDelay || 300);

  const url = useMemo(() => {
    const params = new URLSearchParams();
    if (debouncedQuery) params.set('q', debouncedQuery);
    return `/api/users?${params.toString()}`;
  }, [debouncedQuery]);

  const { data: users, loading, error, refetch } = useFetch(url);

  const { sortedItems, sortKey, sortDirection, toggleSort } = useSort(
    users || [],
    options.initialSortKey,
    options.initialSortDirection || 'asc',
  );

  const {
    paginatedItems,
    currentPage,
    totalPages,
    nextPage,
    prevPage,
    goToPage,
  } = usePagination(sortedItems, options.itemsPerPage || 10);

  return {
    users: paginatedItems,
    loading,
    error,
    sortKey,
    sortDirection,
    toggleSort,
    currentPage,
    totalPages,
    nextPage,
    prevPage,
    goToPage,
    refetch,
  };
}

export default useUserTable;
