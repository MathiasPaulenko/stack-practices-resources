// demo.mjs — runs the review checker against both example schemas.
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { reviewSchema, formatReport } from './review.mjs';

const here = dirname(fileURLToPath(import.meta.url));

for (const name of ['good-schema.graphqls', 'bad-schema.graphqls']) {
  const sdl = readFileSync(join(here, 'schemas', name), 'utf-8');
  const failures = reviewSchema(sdl);
  console.log(`\n=== ${name} ===`);
  console.log(formatReport(failures));
  console.log(`${failures.length} violation(s)`);
}
