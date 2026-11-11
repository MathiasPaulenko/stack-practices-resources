// Generate a styled invoice PDF with Puppeteer + Handlebars.
//
// Demonstrates the two production habits the recipe recommends:
// timeouts on rendering, and browser reuse instead of launch-per-job.
//
// Usage:
//   npm install
//   npx puppeteer browsers install chrome
//   node generate_pdf.js

const puppeteer = require("puppeteer");
const handlebars = require("handlebars");

const template = handlebars.compile(`<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <style>
    body { font-family: Arial, sans-serif; margin: 40px; color: #222; }
    h1 { color: #333; }
    table { border-collapse: collapse; width: 100%; }
    td, th { border: 1px solid #ccc; padding: 8px; text-align: left; }
    .total { font-weight: bold; font-size: 1.2em; }
  </style>
</head>
<body>
  <h1>Invoice #{{invoiceId}}</h1>
  <p>Customer: {{customer}}</p>
  <table>
    <tr><th>Item</th><th>Qty</th><th>Price</th></tr>
    {{#each items}}
    <tr><td>{{name}}</td><td>{{qty}}</td><td>\${{price}}</td></tr>
    {{/each}}
  </table>
  <p class="total">Total: \${{total}}</p>
</body>
</html>`);

async function generatePDF(browser, data, outputPath, timeoutMs = 30000) {
  const page = await browser.newPage();
  try {
    await page.setContent(template(data), {
      waitUntil: "networkidle0",
      timeout: timeoutMs,
    });
    await page.pdf({
      path: outputPath,
      format: "A4",
      printBackground: true,
      timeout: timeoutMs,
    });
    return outputPath;
  } finally {
    await page.close();
  }
}

async function main() {
  const browser = await puppeteer.launch();
  try {
    await generatePDF(
      browser,
      {
        invoiceId: "12345",
        customer: "Acme Corp",
        items: [
          { name: "Consulting", qty: 10, price: "100.00" },
          { name: "Support", qty: 1, price: "250.00" },
        ],
        total: "1,250.00",
      },
      "invoice_12345.pdf"
    );
    console.log("Wrote invoice_12345.pdf");
  } finally {
    await browser.close();
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
