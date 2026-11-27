// Skeletons.jsx — skeleton fallbacks that match the content shape
export function UserCardSkeleton() {
  return (
    <div className="user-card skeleton" aria-busy="true">
      <div className="skeleton-avatar" />
      <div className="skeleton-line w-60" />
      <div className="skeleton-line w-40" />
    </div>
  );
}

export function DashboardSkeleton() {
  return (
    <div className="dashboard skeleton" aria-busy="true">
      <div className="skeleton-header" />
      <div className="skeleton-grid">
        <div className="skeleton-card" />
        <div className="skeleton-card" />
        <div className="skeleton-card" />
      </div>
    </div>
  );
}
