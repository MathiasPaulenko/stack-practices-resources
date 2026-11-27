import { Component, ReactNode } from 'react';

export class ChunkErrorBoundary extends Component<
  { children: ReactNode },
  { failed: boolean }
> {
  state = { failed: false };

  static getDerivedStateFromError() {
    return { failed: true };
  }

  componentDidCatch(error: unknown) {
    if (String(error).match(/chunk|dynamic import/i)) {
      console.warn('Lazy chunk failed; bundle likely stale', error);
    }
  }

  render() {
    if (this.state.failed) {
      return (
        <button onClick={() => location.reload()}>
          Something changed — reload to get the latest version
        </button>
      );
    }
    return this.props.children;
  }
}
