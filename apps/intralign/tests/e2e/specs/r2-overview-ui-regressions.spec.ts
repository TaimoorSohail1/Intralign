import { expect, test } from "@playwright/test";
import { readFileSync } from "node:fs";
import path from "node:path";

const applicationStyles = readFileSync(
  path.resolve(__dirname, "../../../apps/web/src/app/globals.css"),
  "utf8",
);

test.use({ viewport: { width: 2544, height: 1357 } });

test("keeps the frozen first-run Ask OSLO control inside the bounded application shell", async ({
  page,
}) => {
  await page.setContent(`
    <style>${applicationStyles}</style>
    <main class="project-shell is-r2-slice-one is-first-run-frozen">
      <button class="advisor-floating" type="button">
        <span>Ask OSLO</span>
      </button>
    </main>
  `);

  const shell = await page.locator(".project-shell").boundingBox();
  const advisor = await page.locator(".advisor-floating").boundingBox();

  expect(shell).not.toBeNull();
  expect(advisor).not.toBeNull();
  expect(Math.abs(shell!.x + shell!.width - (advisor!.x + advisor!.width))).toBeLessThan(1);
});

test("keeps action feedback the same width and alignment as the issue worklist", async ({
  page,
}) => {
  await page.setContent(`
    <style>${applicationStyles}</style>
    <main class="project-shell is-r2-slice-one">
      <div class="project-grid is-panel-closed">
        <section class="project-main">
          <section class="r2-action-feedback">
            <span>Recorded</span>
            <div><strong>Venue Wi-Fi capacity</strong></div>
            <span>Settling to resolved</span>
          </section>
          <div class="overview-stack has-first-value">
            <section class="start-here">
              <div class="issue-list"><button class="issue-row">Next issue</button></div>
            </section>
          </div>
        </section>
      </div>
    </main>
  `);

  const feedback = await page.locator(".r2-action-feedback").boundingBox();
  const worklist = await page.locator(".issue-list").boundingBox();

  expect(feedback).not.toBeNull();
  expect(worklist).not.toBeNull();
  expect(Math.abs(feedback!.width - worklist!.width)).toBeLessThan(1);
  expect(Math.abs(feedback!.x - worklist!.x)).toBeLessThan(1);
});

test("keeps the collapsed OSLO rail visible and centers Your Outcome in the reading column", async ({
  page,
}) => {
  await page.setContent(`
    <style>${applicationStyles}</style>
    <main class="project-shell is-r2-slice-one is-r2-outcome r2-integrity-without-outcome-anchor">
      <header class="project-header">Header</header>
      <div class="project-grid is-panel-closed">
        <section class="project-main"><div class="your-outcome-dashboard">Your Outcome</div></section>
      </div>
      <button class="advisor-floating" type="button"><span>Ask OSLO</span></button>
    </main>
  `);

  const shell = await page.locator(".project-shell").boundingBox();
  const grid = await page.locator(".project-grid").boundingBox();
  const main = await page.locator(".project-main").boundingBox();
  const advisor = await page.locator(".advisor-floating").boundingBox();

  expect(shell).not.toBeNull();
  expect(grid).not.toBeNull();
  expect(main).not.toBeNull();
  expect(advisor).not.toBeNull();
  expect(advisor!.width).toBe(46);
  expect(advisor!.height).toBeGreaterThan(shell!.height * 0.8);
  expect(Math.abs(shell!.x + shell!.width - (advisor!.x + advisor!.width))).toBeLessThan(1);

  const expectedReadingCenter = grid!.x + (grid!.width - advisor!.width) / 2;
  const actualReadingCenter = main!.x + main!.width / 2;
  expect(Math.abs(expectedReadingCenter - actualReadingCenter)).toBeLessThan(1);
});

test("keeps collapsed read routes flush beneath the shared header", async ({
  page,
}) => {
  await page.setContent(`
    <style>${applicationStyles}</style>
    <main class="project-shell is-r2-slice-one is-r2-outcome r2-integrity-without-outcome-anchor">
      <header class="project-header">Header</header>
      <div class="project-grid is-panel-closed"><section class="project-main">Your Outcome</section></div>
    </main>
  `);

  const collapsedHeader = await page.locator(".project-header").boundingBox();
  const collapsedGrid = await page.locator(".project-grid").boundingBox();
  expect(collapsedHeader).not.toBeNull();
  expect(collapsedGrid).not.toBeNull();
  expect(Math.abs(collapsedHeader!.y + collapsedHeader!.height - collapsedGrid!.y)).toBeLessThan(1);
});

test("sizes the open maturity explanation from its content instead of a fixed tall masthead", async ({
  page,
}) => {
  await page.setContent(`
    <style>${applicationStyles}</style>
    <main class="project-shell is-r2-slice-one r2-integrity-expanded r2-integrity-detail-open r2-integrity-without-outcome-anchor">
      <header class="project-header">Header</header>
      <section class="confidence-read integrity-read">
        <div class="r2-integrity-copy">
          <div class="confidence-topline"><p class="eyebrow">Outcome integrity</p></div>
          <div class="confidence-prototype-hero"><strong>Fragile</strong><div class="r2-integrity-limit-row"><p>limited by Adaptability</p></div></div>
          <div class="r2-maturity-row"><span>Fragile</span><div class="confidence-ramp"><span><i></i></span></div><span>Sound</span></div>
          <details class="confidence-method" open>
            <summary>Why a maturity read, not a probability?</summary>
            <div class="r2-maturity-explanation"><p>Short evidence-based explanation.</p></div>
          </details>
        </div>
        <div class="integrity-pillars"><button>Viability</button><button>Grounding</button><button>Adaptability</button></div>
      </section>
      <div class="project-grid is-panel-closed"><section class="project-main">Issues</section></div>
    </main>
  `);

  const expandedIntegrity = await page.locator(".integrity-read").boundingBox();
  expect(expandedIntegrity).not.toBeNull();
  expect(expandedIntegrity!.height).toBeLessThan(220);
});

test("centers the shared content used by all seven document sections", async ({ page }) => {
  await page.setContent(`
    <style>${applicationStyles}</style>
    <main class="project-shell is-r2-artifact-workspace">
      <header class="project-header">Header</header>
      <div class="project-grid is-panel-closed">
        <section class="project-main">
          <section class="r2-artifact-workspace-open">Workspace open</section>
          <section class="artifact-workspace">Document content</section>
        </section>
      </div>
    </main>
  `);

  const main = await page.locator(".project-main").boundingBox();
  const banner = await page.locator(".r2-artifact-workspace-open").boundingBox();
  const document = await page.locator(".artifact-workspace").boundingBox();

  expect(main).not.toBeNull();
  expect(banner).not.toBeNull();
  expect(document).not.toBeNull();

  const mainCenter = await page.locator(".project-main").evaluate((element) => {
    const rect = element.getBoundingClientRect();
    return rect.left + element.clientLeft + element.clientWidth / 2;
  });
  expect(Math.abs(banner!.x + banner!.width / 2 - mainCenter)).toBeLessThan(1);
  expect(Math.abs(document!.x + document!.width / 2 - mainCenter)).toBeLessThan(1);
});

test("uses the approved success, proposal action, and inline editor styling", async ({
  page,
}) => {
  await page.setContent(`
    <style>${applicationStyles}</style>
    <main class="r2-analysis-page">
      <section class="r2-returning-loader">
        <ol class="r2-returning-trace"><li><span>read inputs</span><i>·</i><strong class="is-complete-status">ok</strong></li></ol>
      </section>
    </main>
    <main class="project-shell is-r2-slice-one is-r2-artifact-workspace">
      <section class="artifact-proposals">
        <article><p>Proposal</p><div><button class="artifact-proposal-accept">Add to plan</button><button class="artifact-proposal-reject">Dismiss</button></div></article>
      </section>
      <div class="r2-statement-row is-editing is-yours">
        <i></i>
        <div><div class="r2-inline-editor"><input value="Run DevNorth 2026"><div><button class="r2-inline-save">Save</button><button class="r2-inline-cancel">Cancel</button></div></div></div>
      </div>
    </main>
  `);

  const statusColor = await page.locator(".is-complete-status").evaluate(
    (element) => getComputedStyle(element).color,
  );
  const acceptBackground = await page.locator(".artifact-proposal-accept").evaluate(
    (element) => getComputedStyle(element).backgroundColor,
  );
  const saveBackground = await page.locator(".r2-inline-save").evaluate(
    (element) => getComputedStyle(element).backgroundColor,
  );
  const editor = await page.locator(".r2-inline-editor input").boundingBox();
  const controls = await page.locator(".r2-inline-editor > div").boundingBox();

  expect(statusColor).toBe("rgb(85, 195, 161)");
  expect(acceptBackground).toBe("rgb(217, 122, 58)");
  expect(saveBackground).toBe("rgb(217, 122, 58)");
  expect(editor).not.toBeNull();
  expect(controls).not.toBeNull();
  expect(controls!.y).toBeGreaterThan(editor!.y + editor!.height);
});

test("aligns every Overview notice to the same 820 pixel reading column", async ({
  page,
}) => {
  await page.setContent(`
    <style>${applicationStyles}.r2-workspace-open { animation: none !important; }</style>
    <main class="project-shell is-r2-slice-one">
      <div class="project-grid is-panel-closed">
        <section class="project-main">
          <section class="r2-action-feedback r2-overview-notice"><span>Recorded</span><div>Status</div><span>Settling</span></section>
          <section class="r2-read-freshness r2-overview-notice"><div>Read status</div></section>
          <section class="r2-read-moved r2-overview-notice"><div>Read updated</div></section>
          <div class="overview-stack has-first-value"><section class="start-here"><section class="r2-workspace-open r2-overview-notice"><span>✦</span><div>Workspace open</div></section></section></div>
        </section>
      </div>
    </main>
  `);

  const notices = await page.locator(".r2-overview-notice").all();
  const boxes = await Promise.all(notices.map((notice) => notice.evaluate((element) => {
    const rect = element.getBoundingClientRect();
    return { x: rect.x, width: rect.width };
  })));

  expect(boxes).toHaveLength(4);
  for (const box of boxes) {
    expect(Math.abs(box.width - boxes[0].width)).toBeLessThan(1);
    expect(Math.abs(box.x - boxes[0].x)).toBeLessThan(1);
  }
});
