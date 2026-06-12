import { defineConfig } from "orval";

// Orval generates the typed API client + TanStack Query hooks from the backend's
// OpenAPI schema. The backend (FastAPI, endpoints/main.py) is the single source of
// the contract — the frontend never hand-writes request/response types.
export default defineConfig({
  oslo: {
    input: {
      // Local: FastAPI serves the schema at /openapi.json (run the backend first).
      target: "http://localhost:8000/openapi.json",
    },
    output: {
      mode: "tags-split",
      target: "./src/api/generated",
      client: "react-query",
      httpClient: "axios",
    },
  },
});
