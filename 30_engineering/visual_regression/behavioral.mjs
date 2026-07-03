// Behavioral gate — invariants the pixel diff can't see (broken tour steps, bare
// Confidence, missing reliability basis). Runs against the reference prototype by
// default; pass --mode app --base <url> to run the same intent against the built app.
//   node behavioral.mjs                       # proto (reference of record)
//   node behavioral.mjs --mode app --base http://localhost:3000
// Exit non-zero on any failed check (CI gate). Each check traces to a decision.
import { chromium } from 'playwright-core';
import { readFileSync } from 'node:fs';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, resolve } from 'node:path';

const HERE = dirname(fileURLToPath(import.meta.url));
const arg = (k, d) => { const i = process.argv.indexOf(k); return i > -1 ? process.argv[i + 1] : d; };
const mode = arg('--mode', 'proto');
const base = arg('--base', process.env.APP_BASE_URL || '');
const cfg  = JSON.parse(readFileSync(resolve(HERE, 'surfaces.json'), 'utf8'));
const protoUrl = pathToFileURL(resolve(HERE, cfg.prototype)).href;

// Checks run in the page context. `setup` navigates/preps; `assert` returns
// { pass:boolean, detail:string }. proto/app split mirrors surfaces.json.
const CHECKS = [
  {
    name: 'tour-integrity',
    trace: 'DL-088/DL-090 — the quick tour must point only at surfaces that exist',
    async run(p) {
      if (mode !== 'proto') return { skip: true, detail: 'app tour is route-driven — adapt per app' };
      await p.goto(protoUrl, { waitUntil: 'load' }); await p.waitForTimeout(300);
      return await p.evaluate(() => {
        if (typeof TOUR === 'undefined' || !Array.isArray(TOUR) || !TOUR.length)
          return { pass: false, detail: 'TOUR array missing or empty' };
        if (typeof jumpToWorkspace === 'function') jumpToWorkspace();
        if (typeof startTour === 'function') startTour();
        const missing = TOUR.map((s, i) => ({ i: i + 1, sel: s.sel, ok: !!document.querySelector(s.sel) }))
                            .filter(r => !r.ok);
        return missing.length
          ? { pass: false, detail: 'unresolved step(s): ' + missing.map(m => `#${m.i} ${m.sel}`).join(', ') }
          : { pass: true, detail: `${TOUR.length} steps all resolve` };
      });
    }
  },
  {
    name: 'confidence-not-bare',
    trace: 'DL-085 — wherever Confidence appears it carries its reliability qualifier',
    async run(p) {
      const url = mode === 'proto' ? protoUrl : base + '/';
      await p.goto(url, { waitUntil: mode === 'proto' ? 'load' : 'networkidle' }); await p.waitForTimeout(300);
      return await p.evaluate(() => {
        const pill = document.getElementById('confpill');
        if (!pill) return { pass: false, detail: '#confpill not found' };
        const t = pill.textContent.toLowerCase();
        return { pass: t.includes('reliab'), detail: t.includes('reliab') ? 'pill shows reliability qualifier' : 'pill has no reliability qualifier (bare Confidence)' };
      });
    }
  },
  {
    name: 'reliability-basis-in-explainer',
    trace: 'DL-090 — Coverage/Evidence/Assessability live in the Confidence explainer',
    async run(p) {
      if (mode !== 'proto') return { skip: true, detail: 'bind to app explainer prep' };
      await p.goto(protoUrl, { waitUntil: 'load' }); await p.waitForTimeout(300);
      return await p.evaluate(() => {
        if (typeof jumpToWorkspace === 'function') jumpToWorkspace();
        if (typeof toggleConfPop === 'function') toggleConfPop({ stopPropagation() {} });
        const pop = document.getElementById('confpop');
        if (!pop || !pop.classList.contains('open')) return { pass: false, detail: 'explainer did not open' };
        const t = pop.textContent.toLowerCase();
        const has = ['reliability basis', 'coverage', 'evidence', 'assess'].filter(k => t.includes(k));
        return { pass: has.length === 4, detail: has.length === 4 ? 'all reliability components present' : 'missing: ' + ['reliability basis','coverage','evidence','assess'].filter(k => !t.includes(k)).join(', ') };
      });
    }
  }
];

const b = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-gpu', '--force-color-profile=srgb'] });
let failed = 0;
for (const c of CHECKS) {
  const p = await b.newPage();
  await p.setViewportSize(cfg.viewport);
  await p.emulateMedia({ reducedMotion: 'reduce' });
  let r;
  try { r = await c.run(p); } catch (e) { r = { pass: false, detail: 'threw: ' + e.message }; }
  await p.close();
  if (r.skip) { console.log(`SKIP ${c.name} — ${r.detail}`); continue; }
  if (r.pass) console.log(`PASS ${c.name} — ${r.detail}`);
  else { failed++; console.log(`FAIL ${c.name} — ${r.detail}  (${c.trace})`); }
}
await b.close();
console.log(failed ? `\nBEHAVIORAL: ${failed} check(s) failed.` : '\nBEHAVIORAL: all checks passed.');
process.exit(failed ? 1 : 0);
