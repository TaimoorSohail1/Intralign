import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  // Dev-only: proxy the API to the local backend so the read surfaces reach :8000
  // (the generated axios client uses relative URLs). Affects `vite dev` only, not
  // `vite build`. Flagged follow-up from DTM-0020.
  server: {
    port: 5173,
    proxy: {
      // Dev-only: attach the dev JWT (OSLO_DEV_TOKEN) so the UI authenticates
      // against the real authenticated backend. No login screen is wired in R1.
      "/v1": {
        target: "http://localhost:8000",
        changeOrigin: true,
        headers: process.env.OSLO_DEV_TOKEN
          ? { Authorization: `Bearer ${process.env.OSLO_DEV_TOKEN}` }
          : undefined,
      },
      "/health": { target: "http://localhost:8000", changeOrigin: true },
      "/openapi.json": { target: "http://localhost:8000", changeOrigin: true },
    },
  },
});
