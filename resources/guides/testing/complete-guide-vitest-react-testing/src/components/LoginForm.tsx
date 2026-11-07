import { FormEvent, useState } from "react";

interface LoginFormProps {
  onSubmit: (credentials: { email: string; password: string }) => void;
}

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function LoginForm({ onSubmit }: LoginFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const next: { email?: string; password?: string } = {};
    if (!email) next.email = "Email is required";
    else if (!EMAIL_RE.test(email)) next.email = "Invalid email format";
    if (!password) next.password = "Password is required";
    setErrors(next);
    if (Object.keys(next).length === 0) onSubmit({ email, password });
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <label htmlFor="email">Email</label>
      <input
        id="email"
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      {errors.email && <p role="alert">{errors.email}</p>}

      <label htmlFor="password">Password</label>
      <input
        id="password"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      {errors.password && <p role="alert">{errors.password}</p>}

      <button type="submit">Submit</button>
    </form>
  );
}
