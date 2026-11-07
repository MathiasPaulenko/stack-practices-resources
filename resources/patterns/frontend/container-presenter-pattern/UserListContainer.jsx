// UserListContainer.jsx — legacy class container (pre-hooks style).
// Kept for reference when migrating older codebases to hooks.
import React, { Component } from 'react';
import { UserListPresenter } from './UserListPresenter';

class UserListContainer extends Component {
  state = { users: [], query: '', loading: true, error: null };

  componentDidMount() { this.fetchUsers(); }

  async fetchUsers() {
    this.setState({ loading: true, error: null });
    try {
      const response = await fetch('/api/users');
      this.setState({ users: await response.json(), loading: false });
    } catch (error) {
      this.setState({ error: error.message, loading: false });
    }
  }

  handleDelete = async (userId) => {
    await fetch(`/api/users/${userId}`, { method: 'DELETE' });
    this.fetchUsers();
  };

  // Store the query and filter at render time — filtering `users` in
  // state would destroy the full list after the first keystroke.
  handleSearch = (query) => this.setState({ query });

  render() {
    const { users, query, loading, error } = this.state;
    const visible = users.filter(u =>
      u.name.toLowerCase().includes(query.toLowerCase())
    );
    return (
      <UserListPresenter
        users={visible}
        loading={loading}
        error={error}
        onDelete={this.handleDelete}
        onSearch={this.handleSearch}
      />
    );
  }
}

export default UserListContainer;
