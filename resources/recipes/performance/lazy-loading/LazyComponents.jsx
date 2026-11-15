import { lazy, Suspense, Component } from 'react';

// lazy() wraps a dynamic import() — the bundler splits HeavyChart and
// VideoPlayer into separate chunks that only download on first render.
const HeavyChart = lazy(() => import('./HeavyChart'));
const VideoPlayer = lazy(() => import('./VideoPlayer'));

// React.lazy throws on render if the chunk fails (e.g. 404 after a new
// deploy). Without an error boundary, that crashes the whole tree.
class ChunkErrorBoundary extends Component {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  render() {
    if (this.state.failed) {
      return (
        <div role="alert">
          <p>Could not load this section.</p>
          <button onClick={() => window.location.reload()}>Reload page</button>
        </div>
      );
    }
    return this.props.children;
  }
}

function SkeletonChart() {
  return <div style={{ height: 320, background: '#e2e8f0', borderRadius: 8 }} />;
}

function SkeletonPlayer() {
  return <div style={{ height: 240, background: '#e2e8f0', borderRadius: 8 }} />;
}

export default function Dashboard() {
  return (
    <div>
      <SummaryCards />
      <ChunkErrorBoundary>
        <Suspense fallback={<SkeletonChart />}>
          <HeavyChart />
        </Suspense>
        <Suspense fallback={<SkeletonPlayer />}>
          <VideoPlayer />
        </Suspense>
      </ChunkErrorBoundary>
    </div>
  );
}
