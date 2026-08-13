import { expect, test } from "../fixtures";
import { mkdirSync, readFileSync } from "node:fs";
import path from "node:path";

test.setTimeout(180_000);

const screenshots = path.resolve(
  __dirname,
  "../../../reports/r2/slice-01/screenshots",
);

async function openAnalyzedProject(page: import("@playwright/test").Page) {
  await page.goto("/login");
  await page.getByLabel("Email").fill("e2e-owner@example.com");
  await page.getByLabel("Password").fill("E2EOwner123!");
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page).toHaveURL(/\/(workspace|welcome)/);
  await page.goto("/workspace");
  const project = page
    .locator("article.workspace-project-card")
    .filter({ hasText: "7 / 7" })
    .first();
  if (await project.count()) {
    await project.getByRole("link", { name: /Open project/ }).click();
  } else {
    await page.goto("/welcome");
    await page.getByRole("button", { name: /Start your first project/ }).click();
    await page.getByRole("button", { name: /sample project/i }).click();
    await page.getByRole("button", { name: /See where I stand/ }).click();
  }
  await expect(page).toHaveURL(/\/projects\/.+\/overview/, { timeout: 120_000 });
  const orientation = page.getByRole("dialog", { name: "How OSLO works" });
  if (await orientation.isVisible()) {
    await orientation.getByRole("button", { name: "Skip", exact: true }).click();
  }
  await expect(page.getByText("Outcome integrity", { exact: true })).toBeVisible();
}

test("R2 Slice 1 exposes the integrity read at every supported viewport", async ({
  page,
}, testInfo) => {
  await openAnalyzedProject(page);

  const integrityRead = page.locator(".integrity-read");
  await expect(integrityRead).toBeVisible();
  await expect(integrityRead.getByText("Fragile", { exact: true }).first()).toBeVisible();
  await expect(integrityRead.getByText("Weak", { exact: true }).first()).toBeVisible();
  await expect(integrityRead.getByText("Developing", { exact: true }).first()).toBeVisible();
  await expect(integrityRead.getByText("Solid", { exact: true }).first()).toBeVisible();
  await expect(integrityRead.getByText("Sound", { exact: true }).first()).toBeVisible();
  await expect(integrityRead.getByRole("button", { name: /^Viability (Fragile|Weak|Developing|Solid|Sound)$/ })).toBeVisible();
  await expect(integrityRead.getByRole("button", { name: /^Grounding (Fragile|Weak|Developing|Solid|Sound)$/ })).toBeVisible();
  await expect(integrityRead.getByRole("button", { name: /^Adaptability (Fragile|Weak|Developing|Solid|Sound)$/ })).toBeVisible();
  await expect(integrityRead).toContainText("live tracking begins at execution");
  await expect(integrityRead).not.toContainText(/\d+%/);

  const horizontalOverflow = await page.evaluate(
    () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
  );
  expect(horizontalOverflow).toBe(false);

  mkdirSync(screenshots, { recursive: true });
  await page.screenshot({
    fullPage: true,
    path: path.join(screenshots, `implementation-${testInfo.project.name}.png`),
  });

  if (testInfo.project.name === "desktop") {
    const mastheadIntegrity = page.getByRole("button", {
      name: /Outcome Integrity .* limited by/,
    });
    await expect(mastheadIntegrity).toContainText(/Viability (Fragile|Weak|Developing|Solid|Sound)/);
    await expect(mastheadIntegrity).toContainText(/Grounding (Fragile|Weak|Developing|Solid|Sound)/);
    await expect(mastheadIntegrity).toContainText(/Adaptability (Fragile|Weak|Developing|Solid|Sound)/);
    await mastheadIntegrity.click();
    const breakdown = page.getByRole("dialog", { name: "Integrity breakdown" });
    await expect(breakdown).toBeVisible();
    await expect(breakdown.getByText("Viability", { exact: true })).toBeVisible();
    await expect(breakdown.getByText("Grounding", { exact: true })).toBeVisible();
    await expect(breakdown.getByText("Adaptability", { exact: true })).toBeVisible();
    await expect(page.getByRole("button", { name: "Close integrity breakdown" })).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(breakdown).toHaveCount(0);
  }
});

test("R2 Slice 1 prototype reference is captured at matching viewports", async ({
  page,
}, testInfo) => {
  const prototype = readFileSync(
    path.resolve(__dirname, "../../../../release-2/oslo-prototype-r2.html"),
    "utf8",
  );
  await page.setContent(prototype, { waitUntil: "domcontentloaded" });
  await page.evaluate(() => {
    const prototypeApp = window as unknown as {
      ARTIFACTS: Array<{ key: string }>;
      ITEMS: Array<{ state: string }>;
      VSTATE: Record<string, string>;
      _CHKPTS: number;
      _everUnlocked: boolean;
      _mhMin: boolean;
      _openId: string | null;
      _primaryOutcome: () => { prov: string } | null;
      applyFreeze: () => void;
      confirmCount: number;
      enterApp: () => void;
      firstRun: boolean;
      focusKey: string | null;
      peeking: boolean;
      render: () => void;
      view: string;
    };
    prototypeApp.enterApp();
    prototypeApp.ITEMS.forEach((item) => {
      item.state = "you";
    });
    prototypeApp.ARTIFACTS.forEach((artifact) => {
      prototypeApp.VSTATE[artifact.key] = "fixed";
    });
    prototypeApp._CHKPTS = 0;
    prototypeApp.firstRun = false;
    prototypeApp.confirmCount = 2;
    prototypeApp._everUnlocked = true;
    prototypeApp.peeking = false;
    prototypeApp.view = "read";
    prototypeApp.focusKey = null;
    prototypeApp._openId = null;
    const outcome = prototypeApp._primaryOutcome();
    if (outcome) outcome.prov = "confirmed";
    prototypeApp._mhMin = false;
    prototypeApp.applyFreeze();
    prototypeApp.render();
  });
  await expect(page.locator(".mh-hero")).toBeVisible();

  mkdirSync(screenshots, { recursive: true });
  await page.screenshot({
    fullPage: true,
    path: path.join(screenshots, `prototype-${testInfo.project.name}.png`),
  });

  const implementationImage = readFileSync(
    path.join(screenshots, `implementation-${testInfo.project.name}.png`),
  ).toString("base64");
  const prototypeImage = readFileSync(
    path.join(screenshots, `prototype-${testInfo.project.name}.png`),
  ).toString("base64");
  await page.setContent(`
    <style>
      * { box-sizing: border-box; }
      body { margin: 0; padding: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; background: #0d1013; color: #eef0f2; font: 700 14px system-ui; }
      figure { min-width: 0; margin: 0; }
      figcaption { margin-bottom: 10px; letter-spacing: .08em; text-transform: uppercase; }
      img { width: 100%; height: auto; display: block; border: 1px solid #39414a; }
    </style>
    <figure><figcaption>R2 prototype reference</figcaption><img alt="R2 prototype reference" src="data:image/png;base64,${prototypeImage}"></figure>
    <figure><figcaption>Executable implementation</figcaption><img alt="Executable implementation" src="data:image/png;base64,${implementationImage}"></figure>
  `);
  await page.screenshot({
    fullPage: true,
    path: path.join(screenshots, `comparison-${testInfo.project.name}.png`),
  });
});
