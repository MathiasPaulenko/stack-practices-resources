import { useState, useCallback, useRef } from 'react';

function useOptimisticState(initialState) {
  const [state, setState] = useState(initialState);
  const [isOptimistic, setIsOptimistic] = useState(false);
  const previousStateRef = useRef(initialState);

  const optimisticUpdate = useCallback(
    async (optimisticState, asyncFn) => {
      previousStateRef.current = state;

      // Apply optimistic state
      setState(optimisticState);
      setIsOptimistic(true);

      try {
        const result = await asyncFn();
        // Server confirmed — keep the state, update with server data if provided
        if (result !== undefined) {
          setState(result);
        }
        setIsOptimistic(false);
        return result;
      } catch (error) {
        // Rollback
        setState(previousStateRef.current);
        setIsOptimistic(false);
        throw error;
      }
    },
    [state]
  );

  return { state, setState, optimisticUpdate, isOptimistic };
}

export default useOptimisticState;
