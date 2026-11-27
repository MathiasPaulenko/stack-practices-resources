// ContactForm.jsx — using the form machine
import { useFormMachine, states } from '../hooks/useFormMachine';

function ContactForm() {
  const { state, data, error, submit, retry, reset } = useFormMachine(
    async (formData) => {
      const response = await fetch('/api/contact', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) throw new Error('Failed to submit');
      return response.json();
    }
  );

  if (state === states.SUCCESS) {
    return (
      <div className="success">
        <h2>Thank you!</h2>
        <p>{data.message}</p>
        <button onClick={reset}>Send another</button>
      </div>
    );
  }

  if (state === states.ERROR) {
    return (
      <div className="error">
        <h2>Submission failed</h2>
        <p>{error}</p>
        <button onClick={retry}>Try again</button>
        <button onClick={reset}>Start over</button>
      </div>
    );
  }

  return (
    <form onSubmit={(e) => {
      e.preventDefault();
      submit(new FormData(e.target));
    }}>
      <input name="email" type="email" required placeholder="Email" />
      <textarea name="message" required placeholder="Message" />
      <button type="submit" disabled={state === states.SUBMITTING}>
        {state === states.SUBMITTING ? 'Sending...' : 'Send'}
      </button>
    </form>
  );
}
