// scripts/check-bundle-size.js
const fs = require('fs');
const path = require('path');
const gzipSize = require('gzip-size');

const budgets = {
  'dist/assets/vendor.js': { max: 100000, type: 'gzipped' },
  'dist/assets/app.js': { max: 50000, type: 'gzipped' },
  'dist/assets/styles.css': { max: 30000, type: 'gzipped' },
};

let failed = false;

for (const [file, budget] of Object.entries(budgets)) {
  const filePath = path.join(process.cwd(), file);
  if (!fs.existsSync(filePath)) {
    console.error(`MISSING: ${file}`);
    failed = true;
    continue;
  }

  const content = fs.readFileSync(filePath);
  const size = budget.type === 'gzipped' ? gzipSize.sync(content) : content.length;
  const sizeKB = (size / 1024).toFixed(1);
  const maxKB = (budget.max / 1024).toFixed(1);

  if (size > budget.max) {
    console.error(`FAIL: ${file} — ${sizeKB} KB (budget: ${maxKB} KB)`);
    failed = true;
  } else {
    console.log(`OK: ${file} — ${sizeKB} KB (budget: ${maxKB} KB)`);
  }
}

if (failed) {
  process.exit(1);
}
