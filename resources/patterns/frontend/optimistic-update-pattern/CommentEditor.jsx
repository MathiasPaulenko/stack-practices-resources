import useOptimisticState from './useOptimisticState.js';

function CommentEditor({ comment }) {
  const { state: text, setState: setText, optimisticUpdate, isOptimistic } =
    useOptimisticState(comment.text);

  const handleSave = async () => {
    try {
      await optimisticUpdate(
        text, // optimistic value, already shown in the textarea
        () => fetch(`/api/comments/${comment.id}`, {
          method: 'PATCH',
          body: JSON.stringify({ text }),
        }).then(res => res.json()).then(data => data.text)
      );
    } catch {
      alert('Failed to save. Reverted to previous text.');
    }
  };

  return (
    <div>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={handleSave} disabled={isOptimistic}>
        {isOptimistic ? 'Saving...' : 'Save'}
      </button>
    </div>
  );
}
