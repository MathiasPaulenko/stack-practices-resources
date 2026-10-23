// Express sitemap generator — manual XML building with escaping + hreflang.
// Requires: express. Swap getProducts() for your real data source.
const express = require("express");
const app = express();

function escapeXml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");
}

function buildSitemap(urls) {
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ];
  for (const url of urls) {
    lines.push("  <url>");
    lines.push(`    <loc>${escapeXml(url.loc)}</loc>`);
    lines.push(`    <lastmod>${url.lastmod}</lastmod>`);
    lines.push(`    <changefreq>${url.changefreq || "weekly"}</changefreq>`);
    lines.push(`    <priority>${url.priority || "0.5"}</priority>`);
    lines.push("  </url>");
  }
  lines.push("</urlset>");
  return lines.join("\n");
}

app.get("/sitemap.xml", (req, res) => {
  const urls = [
    { loc: "https://example.com/", lastmod: "2024-06-01", priority: "1.0" },
    { loc: "https://example.com/blog/post-1", lastmod: "2024-06-10", priority: "0.8" },
  ];
  res.set("Content-Type", "application/xml");
  res.send(buildSitemap(urls));
});

// Paginated sitemap with hreflang annotations
app.get("/sitemap-products.xml", (req, res) => {
  const products = getProducts();
  const lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
  ];
  for (const product of products) {
    lines.push("  <url>");
    lines.push(`    <loc>${escapeXml(product.url)}</loc>`);
    lines.push(`    <lastmod>${product.updatedAt}</lastmod>`);
    for (const lang of ["en", "es", "de"]) {
      lines.push(`    <xhtml:link rel="alternate" hreflang="${lang}"`);
      lines.push(`                href="${escapeXml(product.url)}?lang=${lang}" />`);
    }
    lines.push("  </url>");
  }
  lines.push("</urlset>");
  res.set("Content-Type", "application/xml");
  res.send(lines.join("\n"));
});

function getProducts() {
  return [
    { url: "https://example.com/products/item-1", updatedAt: "2024-06-05" },
    { url: "https://example.com/products/item-2", updatedAt: "2024-06-08" },
  ];
}

app.listen(3000, () => console.log("sitemap on :3000"));
