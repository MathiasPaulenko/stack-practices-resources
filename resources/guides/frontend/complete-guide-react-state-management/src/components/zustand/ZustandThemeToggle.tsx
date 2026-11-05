import { useThemeStore } from "../../stores/useThemeStore";
import { useApplyTheme } from "../../hooks/useApplyTheme";

export function ZustandThemeToggle() {
  // Subscribe to exactly the slices this component needs.
  const theme = useThemeStore((s) => s.theme);
  const toggleTheme = useThemeStore((s) => s.toggleTheme);
  useApplyTheme(theme);

  return (
    <button
      type="button"
      className="theme-toggle"
      aria-pressed={theme === "dark"}
      onClick={toggleTheme}
    >
      Theme: {theme}
    </button>
  );
}
