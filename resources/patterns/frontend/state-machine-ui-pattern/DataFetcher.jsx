// DataFetcher.jsx — using XState with React
import { useMachine } from '@xstate/react';
import fetchMachine from '../machines/fetchMachine';

function DataFetcher({ url }) {
  const [state, send] = useMachine(fetchMachine, {
    services: {
      fetchData: () => fetch(url).then(res => {
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
      }),
    },
  });

  const { data, error, retries } = state.context;

  if (state.matches('idle')) {
    return <button onClick={() => send('FETCH')}>Load data</button>;
  }

  if (state.matches('loading')) {
    return (
      <div>
        <div className="spinner">Loading...</div>
        <button onClick={() => send('CANCEL')}>Cancel</button>
      </div>
    );
  }

  if (state.matches('success')) {
    return (
      <div>
        <pre>{JSON.stringify(data, null, 2)}</pre>
        <button onClick={() => send('REFETCH')}>Refresh</button>
      </div>
    );
  }

  if (state.matches('error')) {
    return (
      <div className="error">
        <p>Error: {error}</p>
        <p>Attempts: {retries}</p>
        {retries < 3 ? (
          <button onClick={() => send('RETRY')}>Retry</button>
        ) : (
          <p>Max retries reached.</p>
        )}
        <button onClick={() => send('RESET')}>Reset</button>
      </div>
    );
  }

  return null;
}
