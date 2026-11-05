import { useState, type ComponentType } from "react";
import { QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "./context/ThemeContext";
import { CartProvider } from "./context/CartContext";
import { queryClient } from "./query/queryClient";
import { ModeTabs, type DemoMode } from "./components/ModeTabs";
import { ProductList } from "./components/ProductList";
import { ContextThemeToggle } from "./components/context/ContextThemeToggle";
import { ContextCartView } from "./components/context/ContextCartView";
import { ContextAddToCartButton } from "./components/context/ContextAddToCartButton";
import { ZustandThemeToggle } from "./components/zustand/ZustandThemeToggle";
import { ZustandCartView } from "./components/zustand/ZustandCartView";
import { ZustandAddToCartButton } from "./components/zustand/ZustandAddToCartButton";
import { JotaiThemeToggle } from "./components/jotai/JotaiThemeToggle";
import { JotaiCartView } from "./components/jotai/JotaiCartView";
import { JotaiAddToCartButton } from "./components/jotai/JotaiAddToCartButton";
import { ServerStateSection } from "./components/query/ServerStateSection";
import type { Product } from "./types";

interface DemoProps {
  mode: DemoMode;
  onModeChange: (mode: DemoMode) => void;
  ThemeToggle: ComponentType;
  CartView: ComponentType;
  AddToCart: ComponentType<{ product: Product }>;
  showServerStateDemo?: boolean;
}

// The same storefront rendered against whichever state implementation the
// active tab selected — the only thing that changes is where state lives.
function Demo({
  mode,
  onModeChange,
  ThemeToggle,
  CartView,
  AddToCart,
  showServerStateDemo,
}: DemoProps) {
  return (
    <div className="demo">
      <ModeTabs mode={mode} onChange={onModeChange} />
      <header className="demo-header">
        <div>
          <h1>React state management playground</h1>
          <p className="muted">
            Same domain — products, cart, theme — wired four different ways.
          </p>
        </div>
        <ThemeToggle />
      </header>
      <main className="demo-grid">
        <ProductList AddToCart={AddToCart} />
        <CartView />
      </main>
      {showServerStateDemo && <ServerStateSection />}
      <footer className="demo-footer">
        <p className="muted">
          Active mode: <strong>{mode}</strong>. Each approach owns its own cart
          and theme state — switching tabs does not migrate it. Products always
          come from the TanStack Query cache because server state belongs in
          the query client, not in a client store.
        </p>
      </footer>
    </div>
  );
}

export default function App() {
  const [mode, setMode] = useState<DemoMode>("context");

  switch (mode) {
    case "context":
      return (
        <QueryClientProvider client={queryClient}>
          <ThemeProvider>
            <CartProvider>
              <Demo
                mode={mode}
                onModeChange={setMode}
                ThemeToggle={ContextThemeToggle}
                CartView={ContextCartView}
                AddToCart={ContextAddToCartButton}
              />
            </CartProvider>
          </ThemeProvider>
        </QueryClientProvider>
      );
    case "zustand":
      return (
        <QueryClientProvider client={queryClient}>
          <Demo
            mode={mode}
            onModeChange={setMode}
            ThemeToggle={ZustandThemeToggle}
            CartView={ZustandCartView}
            AddToCart={ZustandAddToCartButton}
          />
        </QueryClientProvider>
      );
    case "jotai":
      return (
        <QueryClientProvider client={queryClient}>
          <Demo
            mode={mode}
            onModeChange={setMode}
            ThemeToggle={JotaiThemeToggle}
            CartView={JotaiCartView}
            AddToCart={JotaiAddToCartButton}
          />
        </QueryClientProvider>
      );
    case "query":
      // The production combo from the guide's "Putting It Together" section:
      // Context for low-frequency theme state, the Zustand store for the
      // cart, and TanStack Query for everything that comes from the API.
      return (
        <QueryClientProvider client={queryClient}>
          <ThemeProvider>
            <Demo
              mode={mode}
              onModeChange={setMode}
              ThemeToggle={ContextThemeToggle}
              CartView={ZustandCartView}
              AddToCart={ZustandAddToCartButton}
              showServerStateDemo
            />
          </ThemeProvider>
        </QueryClientProvider>
      );
  }
}
