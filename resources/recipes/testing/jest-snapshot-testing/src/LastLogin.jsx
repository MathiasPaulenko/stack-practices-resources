export default function LastLogin({ userId }) {
  const last = new Date();

  return (
    <p className="last-login">
      User {userId} last logged in at {last.toISOString()}
    </p>
  );
}
