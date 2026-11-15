export default function UserProfile({ user, loading = false }) {
  if (loading) {
    return <div className="user-profile user-profile--loading">Loading…</div>;
  }

  return (
    <div className="user-profile">
      <img className="user-profile__avatar" src={user.avatar} alt={`${user.name}'s avatar`} />
      <div className="user-profile__info">
        <h2 className="user-profile__name">{user.name}</h2>
        <p className="user-profile__email">{user.email}</p>
        <span className="user-profile__role">{user.role}</span>
      </div>
    </div>
  );
}
