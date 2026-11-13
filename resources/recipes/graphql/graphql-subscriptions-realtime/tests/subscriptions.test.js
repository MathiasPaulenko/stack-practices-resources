import { describe, it, expect } from 'vitest';
import { resolvers, db } from '../resolvers.mjs';

const ctx = { db, user: { id: 'u1' } };

// The iterator registers its pubsub listener lazily, so prime next()
// before publishing, then await that same promise.
const tick = () => new Promise((r) => setTimeout(r, 0));
const timeout = (ms) => new Promise((r) => setTimeout(() => r('timeout'), ms));

describe('subscription resolvers', () => {
  it('postCreated yields the post the mutation published', async () => {
    const it = resolvers.Subscription.postCreated.subscribe();
    const pending = it.next();
    await tick();
    resolvers.Mutation.createPost(null, { title: 'A', content: 'x' }, ctx);
    const evt = (await pending).value;
    expect(evt.postCreated.title).toBe('A');
    expect(evt.postCreated.authorId).toBe('u1');
  });

  it('postUpdated filters events to the subscribed id', async () => {
    const it = await resolvers.Subscription.postUpdated.subscribe(null, { id: '1' }, ctx);
    const pending = it.next();
    await tick();
    resolvers.Mutation.updatePost(null, { id: '1', title: 'hit' }, ctx);
    const evt = (await pending).value;
    expect(evt.postUpdated.id).toBe('1');
    expect(evt.postUpdated.title).toBe('hit');
  });

  it('postUpdated drops events for other ids', async () => {
    const it = await resolvers.Subscription.postUpdated.subscribe(null, { id: '1' }, ctx);
    await tick();
    // Update a different post; this iterator should stay silent.
    const pending = it.next();
    resolvers.Mutation.updatePost(null, { id: '2', title: 'other' }, ctx);
    expect(await Promise.race([pending, timeout(300)])).toBe('timeout');
    // An update on the subscribed id resolves that same queued pull.
    resolvers.Mutation.updatePost(null, { id: '1', title: 'first' }, ctx);
    const evt = await Promise.race([pending.then((r) => r.value), timeout(500)]);
    expect(evt.postUpdated.title).toBe('first');
    await it.return();
  });

  it('publish uses the subscription field name as payload key', async () => {
    const it = resolvers.Subscription.postCreated.subscribe();
    const pending = it.next();
    await tick();
    resolvers.Mutation.createPost(null, { title: 'B', content: 'y' }, ctx);
    const evt = (await pending).value;
    expect(evt).toHaveProperty('postCreated');
  });
});
