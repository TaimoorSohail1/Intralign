// Capture surface screenshots — from the prototype (baseline) or the built app (candidate).
//   node capture.mjs --mode proto --out baselines
//   node capture.mjs --mode app  --base http://localhost:3000 --out candidate
import { chromium } from 'playwright-core';
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, resolve } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const mode = arg('--mode', 'proto');
const out  = resolve(HERE, arg('--out', mode === 'proto' ? 'baselines' : 'candidate'));
const base = arg('--base', process.env.APP_BASE_URL || '');
const cfg  = JSON.parse(readFileSync(resolve(HERE, 'surfaces.json'), 'utf8'));
mkdirSync(out, { recursive: true });

const protoUrl = pathToFileURL(resolve(HERE, cfg.prototype)).href;
const b = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-gpu', '--force-color-profile=srgb'] });
for (const s of cfg.surfaces) {
  const p = await b.newPage();
  await p.setViewportSize(cfg.viewport);
  await p.emulateMedia({ reducedMotion: 'reduce' });
  if (mode === 'proto') {
    await p.goto(protoUrl, { waitUntil: 'load' }); await p.waitForTimeout(300);
    if (s.proto.prep) await p.evaluate(s.proto.prep);
  } else {
    if (!base) throw new Error('--base or APP_BASE_URL required in app mode');
    await p.goto(base + s.app.path, { waitUntil: 'networkidle' });
    if (s.app && s.app.prep) await p.evaluate(s.app.prep);
  }
  await p.waitForTimeout(500);
  await p.screenshot({ path: `${out}/${s.name}.png`, fullPage: true });
  await p.close();
  console.log('captured', mode, s.name);
}
await b.close();
