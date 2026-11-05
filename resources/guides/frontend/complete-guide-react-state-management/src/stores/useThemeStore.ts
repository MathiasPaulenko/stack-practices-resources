import { create } from "zustand";
import type { Theme } from "../types";

interface ThemeStore {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

// Module-level singleton — no provider needed. Components subscribe to
// slices through selectors, e.g. useThemeStore((s) => s.theme).
export const useThemeStore = create<ThemeStore>()((set) => ({
  theme: "light",
  toggleTheme: () =>
    set((state) => ({
      theme: state.theme === "light" ? "dark" : "light",
    })),
  setTheme: (theme) => set({ theme }),
}));
