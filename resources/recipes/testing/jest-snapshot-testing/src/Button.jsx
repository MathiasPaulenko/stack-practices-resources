export default function Button({ variant = 'primary', disabled = false, children }) {
  return (
    <button className={`btn btn--${variant}`} disabled={disabled}>
      {children}
    </button>
  );
}
