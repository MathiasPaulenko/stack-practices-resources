import { QueryClient } from "@tanstack/react-query";

// Client-level defaults per the guide: a deliberate staleTime so remounts
// don't refetch, a gcTime that keeps inactive queries around, and a single
// retry instead of the aggressive default.
export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000,
      gcTime: 30 * 60 * 1000,
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});
