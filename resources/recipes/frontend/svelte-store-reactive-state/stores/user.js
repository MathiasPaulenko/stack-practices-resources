// stores/user.js — shared session store with persistence
import { writable } from "svelte/store";

const stored =
  typeof localStorage !== "undefined" ? localStorage.getItem("user") : null;

export const user = writable(stored ? JSON.parse(stored) : null);

// Persist on every change (guard for SSR where localStorage is absent)
user.subscribe((value) => {
  if (typeof localStorage === "undefined") return;
  if (value) localStorage.setItem("user", JSON.stringify(value));
  else localStorage.removeItem("user");
});

export async function loginUser(credentials) {
  const response = await fetch("/api/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
  const data = await response.json();
  user.set(data);
  return data;
}

export function logoutUser() {
  user.set(null);
}
