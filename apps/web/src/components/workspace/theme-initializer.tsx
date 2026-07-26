"use client";

import { useEffect } from "react";

export function ThemeInitializer() {
  useEffect(() => {
    const root = document.documentElement;
    const media = window.matchMedia("(prefers-color-scheme: light)");

    const applyTheme = () => {
      const preference = localStorage.getItem("oslo-theme") ?? "system";
      root.dataset.themePreference = preference;
      root.dataset.theme = preference === "system"
        ? (media.matches ? "light" : "dark")
        : preference;
    };

    applyTheme();
    media.addEventListener("change", applyTheme);
    window.addEventListener("storage", applyTheme);

    return () => {
      media.removeEventListener("change", applyTheme);
      window.removeEventListener("storage", applyTheme);
    };
  }, []);

  return null;
}
