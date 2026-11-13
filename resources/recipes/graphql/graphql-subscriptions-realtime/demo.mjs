// End-to-end: start the real server, subscribe over WebSocket,
// fire mutations over HTTP, and print what the subscriber received.
import { createClient } from 'graphql-ws';
import { startServer } from './server.mjs';

const PORT = 4123;
const server = await startServer(PORT);

const client = createClient({ url: `ws://localhost:${PORT}/graphql` });

function subscribe(query, variables = {}) {
  return new Promise((resolve, reject) => {
    const events = [];
    const unsub = client.subscribe(
      { query, variables },
      {
        next: (msg) => { events.push(msg.data); unsub(); resolve(events); },
        error: reject,
        complete: () => resolve(events),
      },
    );
    setTimeout(() => { unsub(); resolve(events); }, 3000);
  });
}

async function httpQuery(query, variables = {}) {
  const res = await fetch(`http://localhost:${PORT}/graphql`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ query, variables }),
  });
  return res.json();
}

// Subscribe first, then trigger the mutation over HTTP.
const subPromise = subscribe(`
  subscription { postCreated { id title authorId } }
`);
await new Promise((r) => setTimeout(r, 300));
const created = await httpQuery(`
  mutation { createPost(title: "Live!", content: "via demo") { id title } }
`);
const createdEvents = await subPromise;

console.log('HTTP mutation result:', JSON.stringify(created.data));
console.log('WS event received:   ', JSON.stringify(createdEvents[0]));

// postUpdated only fires for the id the subscriber asked for.
const updPromise = subscribe(
  `subscription ($id: ID!) { postUpdated(id: $id) { id title } }`,
  { id: '1' },
);
await new Promise((r) => setTimeout(r, 300));
await httpQuery(`mutation { updatePost(id: "2", title: "nope") { id } }`);
await httpQuery(`mutation { updatePost(id: "1", title: "updated!") { id } }`);
const updEvents = await updPromise;
console.log('postUpdated events for id=1 after updating id=2 then id=1:', JSON.stringify(updEvents));

const ok = createdEvents.length === 1 && updEvents.length === 1 && updEvents[0].postUpdated.title === 'updated!';
console.log(ok ? 'PASS: subscription events flowed end to end' : 'FAIL');
await client.dispose();
await server.stop();
process.exit(ok ? 0 : 1);
