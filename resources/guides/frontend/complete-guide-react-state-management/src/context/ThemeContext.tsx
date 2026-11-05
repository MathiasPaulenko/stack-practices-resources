import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useReducer,
  type ReactNode,
} from "react";
import type { Theme } from "../types";
import { useApplyTheme } from "../hooks/useApplyTheme";

type ThemeAction = { type: "toggle" } | { type: "set"; theme: Theme };

function themeReducer(state: Theme, action: ThemeAction): Theme {
  switch (action.type) {
    case "toggle":
      return state === "light" ? "dark" : "light";
    case "set":
      return action.theme;
    default:
      return state;
  }
}

interface ThemeContextValue {
  theme: Theme;
  toggleTheme: () => void;
  setTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, dispatch] = useReducer(themeReducer, "light");

  // dispatch is stable across renders, so these callbacks keep stable
  // identities and the memoized context value only changes with `theme`.
  const toggleTheme = useCallback(() => dispatch({ type: "toggle" }), []);
  const setTheme = useCallback(
    (next: Theme) => dispatch({ type: "set", theme: next }),
    []
  );

  useApplyTheme(theme);

  // Without useMemo, `value` would be a new object every render and React
  // would treat the context as changed — re-rendering every consumer.
  const value = useMemo(
    () => ({ theme, toggleTheme, setTheme }),
    [theme, toggleTheme, setTheme]
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useTheme must be used within a ThemeProvider");
  }
  return context;
}
