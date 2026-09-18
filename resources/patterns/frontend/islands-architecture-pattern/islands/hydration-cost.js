// hydration-cost.js — rough estimator comparing JavaScript shipped
// by full hydration vs. islands architecture.
// Run: node islands/hydration-cost.js

const KB = 1024;

// Example page: a product page where only some components are interactive.
const page = {
  frameworkRuntimeKB: 140,      // React + react-dom, roughly min+gzip
  routerKB: 60,                 // client-side router a SPA would ship
  components: [
    { name: 'Header',          kb: 8,  interactive: false },
    { name: 'ProductGrid',     kb: 25, interactive: false },
    { name: 'SearchBox',       kb: 12, interactive: true },
    { name: 'ProductGallery',  kb: 40, interactive: true },
    { name: 'Reviews',         kb: 18, interactive: false },
    { name: 'NewsletterForm',  kb: 6,  interactive: true },
    { name: 'Footer',          kb: 5,  interactive: false },
  ],
};

const totalComponents = page.components.reduce((n, c) => n + c.kb, 0);
const islandComponents = page.components
  .filter((c) => c.interactive)
  .reduce((n, c) => n + c.kb, 0);

const fullHydration = page.frameworkRuntimeKB + page.routerKB + totalComponents;
const islands = page.frameworkRuntimeKB + islandComponents;

console.log('Component JS total:        ', totalComponents, 'KB');
console.log('Interactive (islands) JS:  ', islandComponents, 'KB');
console.log('---');
console.log('Full hydration ships:      ', fullHydration, 'KB');
console.log('Islands ship:              ', islands, 'KB');
console.log('Savings:                   ', fullHydration - islands, 'KB',
  `(${Math.round((1 - islands / fullHydration) * 100)}% less JS)`);
