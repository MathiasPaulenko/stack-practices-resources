// UserListPresenter.jsx — presenter for the legacy class container.
import React from 'react';
import PropTypes from 'prop-types';

export function UserListPresenter({ users, loading, error, onDelete, onSearch }) {
  if (loading) return <div className="spinner">Loading users...</div>;
  if (error) return <div className="error">Failed to load: {error}</div>;

  return (
    <div className="user-list">
      <input
        type="search"
        placeholder="Search users..."
        onChange={(e) => onSearch(e.target.value)}
      />
      <ul>
        {users.map(user => (
          <li key={user.id}>
            <span>{user.name} — {user.email}</span>
            <button onClick={() => onDelete(user.id)}>Delete</button>
          </li>
        ))}
      </ul>
      {users.length === 0 && <p>No users found.</p>}
    </div>
  );
}

UserListPresenter.propTypes = {
  users: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    name: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
  })).isRequired,
  loading: PropTypes.bool.isRequired,
  error: PropTypes.string,
  onDelete: PropTypes.func.isRequired,
  onSearch: PropTypes.func.isRequired,
};
