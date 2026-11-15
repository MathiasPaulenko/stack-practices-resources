export default function Badge({ status = 'default', children }) {
  return <span className={`badge badge--${status}`}>{children}</span>;
}
