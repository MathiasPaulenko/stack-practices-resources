import { useEffect } from "react";
import type { Theme } from "../types";

// Applies the active theme to <html data-theme="..."> so the CSS variables
// switch the whole demo no matter which state tool owns the value.
export function useApplyTheme(theme: Theme) {
  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);
}
