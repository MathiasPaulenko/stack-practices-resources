export type DemoMode = "context" | "zustand" | "jotai" | "query";

const MODES: { id: DemoMode; label: string; hint: string }[] = [
  { id: "context", label: "Context API", hint: "useReducer + useMemo" },
  { id: "zustand", label: "Zustand", hint: "selectors + persist" },
  { id: "jotai", label: "Jotai", hint: "atoms + atomFamily" },
  { id: "query", label: "TanStack Query", hint: "server state + combo" },
];

export function ModeTabs({
  mode,
  onChange,
}: {
  mode: DemoMode;
  onChange: (mode: DemoMode) => void;
}) {
  return (
    <nav className="mode-tabs" aria-label="State management approach">
      {MODES.map((entry) => (
        <button
          key={entry.id}
          type="button"
          className={mode === entry.id ? "mode-tab active" : "mode-tab"}
          aria-pressed={mode === entry.id}
          onClick={() => onChange(entry.id)}
        >
          <strong>{entry.label}</strong>
          <span>{entry.hint}</span>
        </button>
      ))}
    </nav>
  );
}
