// Compare candidate/ vs baselines/ per surface; write diffs/; fail if any surface
// exceeds diffThreshold (fraction of differing pixels). Exit 1 on failure.
//   node compare.mjs
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';
import { PNG } from 'pngjs';
import pixelmatch from 'pixelmatch';

const HERE = dirname(fileURLToPath(import.meta.url));
const cfg = JSON.parse(readFileSync(resolve(HERE, 'surfaces.json'), 'utf8'));
const baseDir = resolve(HERE, 'baselines');
const candDir = resolve(HERE, 'candidate');
const diffDir = resolve(HERE, 'diffs'); mkdirSync(diffDir, { recursive: true });

let failed = 0;
for (const s of cfg.surfaces) {
  const bp = `${baseDir}/${s.name}.png`, cp = `${candDir}/${s.name}.png`;
  if (!existsSync(cp)) { console.log(`FAIL ${s.name} — no candidate (surface not rendered by the app?)`); failed++; continue; }
  const a = PNG.sync.read(readFileSync(bp));
  const b = PNG.sync.read(readFileSync(cp));
  if (a.width !== b.width || a.height !== b.height) {
    console.log(`FAIL ${s.name} — size ${b.width}x${b.height} != baseline ${a.width}x${a.height}`); failed++; continue;
  }
  const diff = new PNG({ width: a.width, height: a.height });
  const px = pixelmatch(a.data, b.data, diff.data, a.width, a.height, { threshold: 0.1 });
  const ratio = px / (a.width * a.height);
  writeFileSync(`${diffDir}/${s.name}.png`, PNG.sync.write(diff));
  const ok = ratio <= cfg.diffThreshold;
  console.log(`${ok ? 'PASS' : 'FAIL'} ${s.name} — ${(ratio * 100).toFixed(3)}% diff (threshold ${(cfg.diffThreshold * 100).toFixed(1)}%)`);
  if (!ok) failed++;
}
console.log(failed ? `\nVISUAL REGRESSION: ${failed} surface(s) failed. See diffs/.` : '\nVISUAL REGRESSION: all surfaces within threshold.');
process.exit(failed ? 1 : 0);
