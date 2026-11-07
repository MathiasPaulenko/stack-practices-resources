// tests/components/ThemeAwareComponent.test.tsx — Context mocking
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import { ThemeContext, Theme } from "@/contexts/ThemeContext";
import { ThemeAwareComponent } from "@/components/ThemeAwareComponent";

function renderWithTheme(ui: React.ReactNode, theme: Theme = "light") {
  return render(
    <ThemeContext.Provider value={{ theme, toggleTheme: vi.fn() }}>
      {ui}
    </ThemeContext.Provider>
  );
}

describe("ThemeAwareComponent", () => {
  it("renders light theme styles", () => {
    renderWithTheme(<ThemeAwareComponent />, "light");
    expect(screen.getByTestId("themed")).toHaveClass("light");
  });

  it("renders dark theme styles", () => {
    renderWithTheme(<ThemeAwareComponent />, "dark");
    expect(screen.getByTestId("themed")).toHaveClass("dark");
  });
});
