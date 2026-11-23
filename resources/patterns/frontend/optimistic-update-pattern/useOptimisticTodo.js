import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';

function useTodos() {
  const queryClient = useQueryClient();

  const { data: todos = [] } = useQuery({
    queryKey: ['todos'],
    queryFn: () => fetch('/api/todos').then(res => res.json()),
  });

  const addTodoMutation = useMutation({
    mutationFn: (text) =>
      fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      }).then(res => res.json()),

    onMutate: async (text) => {
      // Cancel outgoing refetches
      await queryClient.cancelQueries({ queryKey: ['todos'] });

      // Snapshot previous value
      const previousTodos = queryClient.getQueryData(['todos']);

      // Optimistically add
      queryClient.setQueryData(['todos'], (old) => [
        ...old,
        { id: crypto.randomUUID(), text, completed: false, pending: true },
      ]);

      // Return context with previous value
      return { previousTodos };
    },

    onError: (err, text, context) => {
      // Rollback on error
      queryClient.setQueryData(['todos'], context.previousTodos);
    },

    onSettled: () => {
      // Always refetch after error or success
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  const deleteTodoMutation = useMutation({
    mutationFn: (id) =>
      fetch(`/api/todos/${id}`, { method: 'DELETE' }),

    onMutate: async (id) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previousTodos = queryClient.getQueryData(['todos']);

      queryClient.setQueryData(['todos'], (old) =>
        old.filter((t) => t.id !== id)
      );

      return { previousTodos };
    },

    onError: (err, id, context) => {
      queryClient.setQueryData(['todos'], context.previousTodos);
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  const toggleTodoMutation = useMutation({
    mutationFn: ({ id, completed }) =>
      fetch(`/api/todos/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed }),
      }),

    onMutate: async ({ id, completed }) => {
      await queryClient.cancelQueries({ queryKey: ['todos'] });
      const previousTodos = queryClient.getQueryData(['todos']);

      queryClient.setQueryData(['todos'], (old) =>
        old.map((t) => t.id === id ? { ...t, completed } : t)
      );

      return { previousTodos };
    },

    onError: (err, variables, context) => {
      queryClient.setQueryData(['todos'], context.previousTodos);
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: ['todos'] });
    },
  });

  return {
    todos,
    addTodo: addTodoMutation.mutate,
    deleteTodo: deleteTodoMutation.mutate,
    toggleTodo: toggleTodoMutation.mutate,
    isAdding: addTodoMutation.isPending,
  };
}

export default useTodos;
