// Renders catalogo_dentmed.html to catalogo_dentmed.pdf (A4, print background).
// Usage: node render.js
// Requires the "playwright" package with Chromium installed
// (npx playwright install chromium, if you don't already have a browser).
const path = require('path');
const { chromium } = require('playwright');

(async () => {
  const dir = __dirname;
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.goto('file://' + path.join(dir, 'catalogo_dentmed.html'), { waitUntil: 'networkidle' });
  await page.pdf({
    path: path.join(dir, 'catalogo_dentmed.pdf'),
    format: 'A4',
    printBackground: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });
  await browser.close();
  console.log('wrote', path.join(dir, 'catalogo_dentmed.pdf'));
})();
