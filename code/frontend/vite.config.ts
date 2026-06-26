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
      "/v1": { target: "http://localhost:8000", changeOrigin: true },
      "/health": { target: "http://localhost:8000", changeOrigin: true },
      "/openapi.json": { target: "http://localhost:8000", changeOrigin: true },
    },
  },
});
