import { useAtomValue, useSetAtom } from "jotai";
import { themeAtom, toggleThemeAtom } from "../../atoms/themeAtoms";
import { useApplyTheme } from "../../hooks/useApplyTheme";

export function JotaiThemeToggle() {
  // Each hook subscribes to a different granularity: the value, and the
  // write-only action atom.
  const theme = useAtomValue(themeAtom);
  const toggleTheme = useSetAtom(toggleThemeAtom);
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
