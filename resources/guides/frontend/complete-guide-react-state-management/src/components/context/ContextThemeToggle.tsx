import { useTheme } from "../../context/ThemeContext";

export function ContextThemeToggle() {
  const { theme, toggleTheme } = useTheme();
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
