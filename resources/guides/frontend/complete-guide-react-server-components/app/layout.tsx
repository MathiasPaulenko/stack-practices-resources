import type { Metadata } from "next";
import type { ReactNode } from "react";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: {
    default: "RSC Playground",
    template: "%s — RSC Playground",
  },
  description:
    "Executable companion to the React Server Components guide: App Router, server actions, streaming, and error boundaries.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="border-b border-zinc-200 bg-white">
          <nav className="mx-auto flex max-w-6xl items-center gap-6 px-6 py-3 text-sm">
            <Link href="/" className="font-semibold text-zinc-900">
              RSC Playground
            </Link>
            <Link href="/products" className="text-zinc-600 hover:text-zinc-900">
              Products
            </Link>
          </nav>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
