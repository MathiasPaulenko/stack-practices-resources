import React, { useState, useOptimistic, startTransition } from 'react';

function OptimisticTodo({ initialTodos }) {
  const [todos, setTodos] = useState(initialTodos);
  const [optimisticTodos, addOptimisticTodo] = useOptimistic(
    todos,
    (current, newTodo) => [...current, { ...newTodo, pending: true }]
  );

  const addTodo = (formData) => {
    const text = formData.get('text');
    const tempTodo = { id: crypto.randomUUID(), text, completed: false };

    startTransition(async () => {
      addOptimisticTodo(tempTodo); // shown instantly, rolls back if the action throws
      const res = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      if (!res.ok) throw new Error('Add failed');
      const saved = await res.json();
      setTodos(prev => [...prev, saved]); // commit the real state on success
    });
  };

  return (
    <form action={addTodo}>
      <input name="text" placeholder="New todo..." />
      <ul>
        {optimisticTodos.map(t => (
          <li key={t.id} style={{ opacity: t.pending ? 0.5 : 1 }}>{t.text}</li>
        ))}
      </ul>
    </form>
  );
}
