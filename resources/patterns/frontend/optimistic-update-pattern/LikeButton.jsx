import React, { useState } from 'react';

function LikeButton({ postId, initialLiked, initialCount }) {
  const [liked, setLiked] = useState(initialLiked);
  const [count, setCount] = useState(initialCount);
  const [error, setError] = useState(null);

  const handleLike = async () => {
    const previousLiked = liked;
    const previousCount = count;

    // Optimistic update — immediate UI change
    setLiked(!liked);
    setCount(prev => liked ? prev - 1 : prev + 1);
    setError(null);

    try {
      const response = await fetch(`/api/posts/${postId}/like`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ liked: !liked }),
      });

      if (!response.ok) throw new Error('Failed to update like');

      // Server confirmed — UI was already correct
    } catch (err) {
      // Rollback to previous state
      setLiked(previousLiked);
      setCount(previousCount);
      setError('Could not update like. Please try again.');
    }
  };

  return (
    <div className="like-button">
      <button onClick={handleLike} className={liked ? 'liked' : ''}>
        {liked ? '♥' : '♡'} {count}
      </button>
      {error && <span className="error-text">{error}</span>}
    </div>
  );
}

export default LikeButton;
