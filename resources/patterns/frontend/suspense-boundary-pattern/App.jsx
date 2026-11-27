// App.jsx — nested Suspense boundaries with an error boundary
import React, { Suspense, lazy } from 'react';
import ErrorBoundary from './ErrorBoundary';
import { fetchUser } from './suspenseResource';
import { UserCardSkeleton, DashboardSkeleton } from './Skeletons';

const HeavyChart = lazy(() => import('./HeavyChart'));

function UserCard({ userId }) {
  const user = fetchUser(userId).read();
  return (
    <div className="user-card">
      <img src={user.avatar} alt={user.name} />
      <h3>{user.name}</h3>
      <p>{user.role}</p>
    </div>
  );
}

export default function App() {
  return (
    <ErrorBoundary>
      <div className="page">
        <h1>Dashboard</h1>

        <Suspense fallback={<UserCardSkeleton />}>
          <UserCard userId={42} />
        </Suspense>

        <Suspense fallback={<DashboardSkeleton />}>
          <HeavyChart />
        </Suspense>
      </div>
    </ErrorBoundary>
  );
}
