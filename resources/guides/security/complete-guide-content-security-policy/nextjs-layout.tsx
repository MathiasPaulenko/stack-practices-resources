// app/layout.tsx — Next.js App Router
// Reads the nonce set by middleware and passes it to scripts.
// Note: reading headers() makes the route dynamic — the trade-off
// that per-request nonces impose everywhere.
import { headers } from 'next/headers';
import Script from 'next/script';

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  const nonce = (await headers()).get('x-nonce');
  return (
    <html lang="en">
      <body>
        {children}
        <Script
          src="https://cdn.example.com/app.js"
          nonce={nonce ?? undefined}
          strategy="beforeInteractive"
        />
      </body>
    </html>
  );
}
