// vite-plugin-brotli.js
// Vite plugin to pre-compress static assets with Brotli at build time
import { brotliCompressSync } from 'zlib';
import { readFileSync, writeFileSync, readdirSync, statSync } from 'fs';
import { resolve, extname } from 'path';

const EXTENSIONS = ['.js', '.css', '.html', '.svg', '.json'];

function compressDir(dir) {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = resolve(dir, entry.name);
    if (entry.isDirectory()) {
      compressDir(full);
    } else if (EXTENSIONS.includes(extname(entry.name))) {
      const compressed = brotliCompressSync(readFileSync(full));
      writeFileSync(`${full}.br`, compressed);
    }
  }
}

export default function brotliPlugin() {
  return {
    name: 'brotli-precompress',
    closeBundle() {
      const dist = resolve('dist');
      if (!statSync(dist).isDirectory()) return;
      compressDir(dist);
      console.log('Brotli pre-compression complete');
    },
  };
}
