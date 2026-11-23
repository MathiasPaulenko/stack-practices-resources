function BulkComplete({ selectedIds, todos, setTodos }) {
  const [error, setError] = useState(null);

  const handleBulkComplete = async () => {
    const previousTodos = [...todos];

    // Optimistic: mark all selected as completed
    setTodos(prev =>
      prev.map(t =>
        selectedIds.includes(t.id) ? { ...t, completed: true } : t
      )
    );

    try {
      await fetch('/api/todos/bulk-complete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids: selectedIds }),
      });
    } catch {
      // Rollback all
      setTodos(previousTodos);
      setError('Failed to complete some items.');
    }
  };

  return (
    <button onClick={handleBulkComplete}>
      Complete {selectedIds.length} items
    </button>
  );
}
