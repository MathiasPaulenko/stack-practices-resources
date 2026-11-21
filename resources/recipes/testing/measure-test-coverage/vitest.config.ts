// Vitest 1.x+: thresholds live under coverage.thresholds, not at coverage root.
import { defineConfig } from 'vitest/config';

export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'html', 'json', 'lcov'],
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 75,
        statements: 80,
      },
      exclude: [
        '**/*.test.ts',
        '**/tests/**',
        '**/node_modules/**',
        '**/vendor/**',
      ],
    },
  },
});
