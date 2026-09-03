import { cleanup, render, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import { ThemeInitializer } from "./theme-initializer";

function stubLightSystemTheme() {
  vi.stubGlobal("matchMedia", vi.fn().mockReturnValue({
    matches: true,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
  }));
}

describe("ThemeInitializer", () => {
  afterEach(() => {
    cleanup();
    localStorage.clear();
    document.documentElement.removeAttribute("data-theme");
    document.documentElement.removeAttribute("data-theme-preference");
    vi.unstubAllGlobals();
  });

  it("defaults a first-time browser to dark even when the device theme is light", async () => {
    stubLightSystemTheme();

    render(<ThemeInitializer />);

    await waitFor(() => expect(document.documentElement.dataset.theme).toBe("dark"));
    expect(document.documentElement.dataset.themePreference).toBe("dark");
    expect(localStorage.getItem("oslo-theme")).toBe("dark");
  });

  it("preserves an explicit saved light preference", async () => {
    stubLightSystemTheme();
    localStorage.setItem("oslo-theme", "light");

    render(<ThemeInitializer />);

    await waitFor(() => expect(document.documentElement.dataset.theme).toBe("light"));
    expect(document.documentElement.dataset.themePreference).toBe("light");
  });

  it("preserves an explicit saved system preference", async () => {
    stubLightSystemTheme();
    localStorage.setItem("oslo-theme", "system");

    render(<ThemeInitializer />);

    await waitFor(() => expect(document.documentElement.dataset.theme).toBe("light"));
    expect(document.documentElement.dataset.themePreference).toBe("system");
  });
});
