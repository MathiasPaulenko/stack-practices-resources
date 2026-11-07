import { useState, useMemo } from 'react';

/** Client-side pagination over an array. */
export function usePagination(items, itemsPerPage = 10) {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(items.length / itemsPerPage);

  const paginatedItems = useMemo(() => {
    const start = (currentPage - 1) * itemsPerPage;
    return items.slice(start, start + itemsPerPage);
  }, [items, currentPage, itemsPerPage]);

  const nextPage = () => setCurrentPage((prev) => Math.min(prev + 1, totalPages));
  const prevPage = () => setCurrentPage((prev) => Math.max(prev - 1, 1));
  const goToPage = (page) =>
    setCurrentPage(Math.min(Math.max(page, 1), totalPages));

  return {
    paginatedItems,
    currentPage,
    totalPages,
    nextPage,
    prevPage,
    goToPage,
  };
}

export default usePagination;
