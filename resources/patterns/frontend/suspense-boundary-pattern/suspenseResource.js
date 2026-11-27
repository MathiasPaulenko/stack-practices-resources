// suspenseResource.js — minimal suspense-compatible data source with cache
// wrapPromise turns a promise into a resource useable with <Suspense>
export function wrapPromise(promise) {
  let status = 'pending';
  let result;
  const suspender = promise.then(
    (r) => {
      status = 'success';
      result = r;
    },
    (e) => {
      status = 'error';
      result = e;
    }
  );

  return {
    read() {
      if (status === 'pending') throw suspender;
      if (status === 'error') throw result;
      return result;
    },
  };
}

// Simple cache so re-renders don't create new promises and suspend forever
const cache = new Map();

export function fetchUser(userId) {
  const key = `user:${userId}`;
  if (!cache.has(key)) {
    cache.set(
      key,
      wrapPromise(
        fetch(`/api/users/${userId}`).then((res) => {
          if (!res.ok) throw new Error(`HTTP ${res.status}`);
          return res.json();
        })
      )
    );
  }
  return cache.get(key);
}
