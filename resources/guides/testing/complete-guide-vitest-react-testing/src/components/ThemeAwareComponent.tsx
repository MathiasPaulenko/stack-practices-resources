import { useContext } from "react";
import { ThemeContext } from "@/contexts/ThemeContext";

export function ThemeAwareComponent() {
  const { theme } = useContext(ThemeContext);
  return (
    <div data-testid="themed" className={theme}>
      Theme-aware content
    </div>
  );
}
