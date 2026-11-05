import {
  keepPreviousData,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { createProduct, fetchProducts, fetchProductsPage } from "../api";
import type { NewProduct, PaginatedProducts, Product } from "../types";

// The query key is the cache address — every hook using ["products"] shares
// one request, one cache entry, and one lifecycle (dedup for free).
export const productsQueryKey = ["products"] as const;

export function useProducts() {
  return useQuery({
    queryKey: productsQueryKey,
    queryFn: fetchProducts,
    staleTime: 5 * 60 * 1000, // fresh for 5 minutes — no refetch on remount
  });
}

export function usePaginatedProducts(page: number) {
  return useQuery<PaginatedProducts>({
    queryKey: [...productsQueryKey, "page", page],
    queryFn: () => fetchProductsPage(page),
    // Keep the previous page visible while the next one loads — without
    // this every page turn flashes a spinner and the list collapses.
    placeholderData: keepPreviousData,
  });
}

interface CreateProductVariables {
  product: NewProduct;
  simulateError?: boolean;
}

export function useCreateProduct() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ product, simulateError }: CreateProductVariables) =>
      createProduct(product, { fail: simulateError }),

    // snapshot -> mutate -> settle: append an optimistic row, roll back on
    // error, and resync with the server either way.
    onMutate: async ({ product }) => {
      // Cancel in-flight refetches so they can't overwrite the optimistic write.
      await queryClient.cancelQueries({ queryKey: productsQueryKey });

      // Snapshot the previous value for rollback.
      const previousProducts =
        queryClient.getQueryData<Product[]>(productsQueryKey);

      // Write the new row straight into the cache — the UI updates instantly.
      const optimistic: Product = {
        ...product,
        id: `temp-${Date.now()}`,
      };
      queryClient.setQueryData<Product[]>(productsQueryKey, (old) => [
        ...(old ?? []),
        optimistic,
      ]);

      // Return context so onError can restore the snapshot.
      return { previousProducts };
    },

    onError: (_error, _variables, context) => {
      // Server rejected the write — put the old data back.
      queryClient.setQueryData(productsQueryKey, context?.previousProducts);
    },

    onSettled: () => {
      // Whether it succeeded or failed, resync with the server. The
      // ["products"] prefix also invalidates the paginated queries.
      queryClient.invalidateQueries({ queryKey: productsQueryKey });
    },
  });
}
