import React, { useState } from 'react';

function TodoList({ initialTodos }) {
  const [todos, setTodos] = useState(initialTodos);
  const [error, setError] = useState(null);

  const addTodo = async (text) => {
    const tempId = crypto.randomUUID();
    const newTodo = { id: tempId, text, completed: false, pending: true };

    // Optimistic add
    setTodos(prev => [...prev, newTodo]);
    setError(null);

    try {
      const response = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text }),
      });
      const savedTodo = await response.json();

      // Replace temp todo with server todo
      setTodos(prev =>
        prev.map(t => t.id === tempId ? { ...savedTodo, pending: false } : t)
      );
    } catch (err) {
      // Rollback — remove the temp todo
      setTodos(prev => prev.filter(t => t.id !== tempId));
      setError('Failed to add todo. Please try again.');
    }
  };

  const deleteTodo = async (id) => {
    const previousTodos = todos;

    // Optimistic delete
    setTodos(prev => prev.filter(t => t.id !== id));
    setError(null);

    try {
      const response = await fetch(`/api/todos/${id}`, { method: 'DELETE' });
      if (!response.ok) throw new Error('Delete failed');
    } catch (err) {
      // Rollback
      setTodos(previousTodos);
      setError('Failed to delete. Please try again.');
    }
  };

  const toggleTodo = async (id) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return;

    // Optimistic toggle
    setTodos(prev =>
      prev.map(t => t.id === id ? { ...t, completed: !t.completed } : t)
    );

    try {
      const response = await fetch(`/api/todos/${id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ completed: !todo.completed }),
      });
      if (!response.ok) throw new Error('Toggle failed');
    } catch (err) {
      // Rollback
      setTodos(prev =>
        prev.map(t => t.id === id ? { ...t, completed: todo.completed } : t)
      );
      setError('Failed to update. Please try again.');
    }
  };

  return (
    <div className="todo-list">
      <form onSubmit={(e) => {
        e.preventDefault();
        const input = e.target.elements.text;
        if (input.value.trim()) {
          addTodo(input.value.trim());
          input.value = '';
        }
      }}>
        <input name="text" placeholder="New todo..." />
        <button type="submit">Add</button>
      </form>

      {error && <div className="error">{error}</div>}

      <ul>
        {todos.map(todo => (
          <li key={todo.id} className={todo.pending ? 'pending' : ''}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleTodo(todo.id)}
            />
            <span style={{ textDecoration: todo.completed ? 'line-through' : '' }}>
              {todo.text}
            </span>
            <button onClick={() => deleteTodo(todo.id)}>×</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TodoList;
