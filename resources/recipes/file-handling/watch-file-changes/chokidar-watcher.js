// Chokidar watcher with filtering, debounce, and stable-write detection.
// Requires: npm install chokidar
// Usage:    node chokidar-watcher.js [directory]

const chokidar = require('chokidar');

const watchDir = process.argv[2] || './src';

const watcher = chokidar.watch(watchDir, {
    ignored: /(^|[\/\\])\./,  // ignore dotfiles
    persistent: true,
    ignoreInitial: true,
    followSymlinks: false,
    awaitWriteFinish: {
        stabilityThreshold: 500,
        pollInterval: 100,
    },
});

const debounce = new Map();
function debouncedRun(file, fn, delay = 300) {
    if (debounce.has(file)) clearTimeout(debounce.get(file));
    debounce.set(file, setTimeout(() => {
        fn(file);
        debounce.delete(file);
    }, delay));
}

watcher
    .on('add', file => debouncedRun(file, f => {
        if (f.endsWith('.csv')) processCSV(f);
    }))
    .on('change', file => debouncedRun(file, f => {
        if (f.endsWith('.js')) rebuildBundle(f);
        if (f.endsWith('.css')) recompileStyles(f);
    }))
    .on('unlink', file => {
        console.log(`Deleted: ${file}`);
        cleanupCache(file);
    })
    .on('error', err => console.error('Watcher error:', err))
    .on('ready', () => console.log(`Initial scan complete. Watching ${watchDir} for changes...`));

function processCSV(file) { console.log(`Processing CSV: ${file}`); }
function rebuildBundle(file) { console.log(`Rebuilding: ${file}`); }
function recompileStyles(file) { console.log(`Recompiling CSS: ${file}`); }
function cleanupCache(file) { console.log(`Cleaning cache for: ${file}`); }

// Cleanup on exit
process.on('SIGINT', () => watcher.close().then(() => process.exit(0)));
