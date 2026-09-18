// NewsletterForm.jsx — a non-critical island hydrated on client:idle.
// It works as a plain HTML form even before hydration finishes.
import { useState } from 'react';

export default function NewsletterForm() {
  const [status, setStatus] = useState('idle');

  const submit = async (e) => {
    e.preventDefault();
    setStatus('sending');
    const email = new FormData(e.target).get('email');
    await fetch('/api/newsletter', {
      method: 'POST',
      body: JSON.stringify({ email }),
      headers: { 'Content-Type': 'application/json' },
    });
    setStatus('done');
  };

  if (status === 'done') return <p>Thanks — check your inbox.</p>;

  return (
    <form onSubmit={submit} action="/api/newsletter" method="post">
      <input name="email" type="email" required placeholder="you@example.com" />
      <button type="submit" disabled={status === 'sending'}>
        {status === 'sending' ? 'Subscribing…' : 'Subscribe'}
      </button>
    </form>
  );
}
