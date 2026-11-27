import { lazy, Suspense } from 'react';
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom';
import { ChunkErrorBoundary } from './components/ChunkErrorBoundary';
import { prefetchRoute } from './utils/prefetch';

const Dashboard = lazy(() => import('./pages/Dashboard'));
const Reports = lazy(() => import('./pages/Reports'));
const Analytics = lazy(() => import('./pages/Analytics'));

export function App() {
  return (
    <BrowserRouter>
      <nav>
        <Link to="/">Dashboard</Link>{' '}
        <Link to="/reports" onMouseEnter={() => prefetchRoute('/reports')}>
          Reports
        </Link>{' '}
        <Link to="/analytics" onMouseEnter={() => prefetchRoute('/analytics')}>
          Analytics
        </Link>
      </nav>
      <ChunkErrorBoundary>
        <Suspense fallback={<p>Loading…</p>}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/reports" element={<Reports />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </Suspense>
      </ChunkErrorBoundary>
    </BrowserRouter>
  );
}
