import { atom } from "jotai";
import type { Theme } from "../types";

// Primitive atom — a single value any component can subscribe to.
export const themeAtom = atom<Theme>("light");

// Write-only derived atoms expose actions without a store object — the
// Jotai equivalent of the `toggleTheme` function in the other demos.
export const toggleThemeAtom = atom(null, (get, set) => {
  set(themeAtom, get(themeAtom) === "light" ? "dark" : "light");
});

export const setThemeAtom = atom(null, (_get, set, theme: Theme) => {
  set(themeAtom, theme);
});
