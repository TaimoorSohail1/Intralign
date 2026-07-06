import { defineConfig } from "orval";

// Orval generates the typed API client + TanStack Query hooks from the backend's
// OpenAPI schema. The backend (FastAPI, endpoints/main.py) is the single source of
// the contract — the frontend never hand-writes request/response types.
export default defineConfig({
  oslo: {
    input: {
      // Offline, deterministic codegen: read the schema from a dumped file, not a
      // live backend (CI never starts localhost:8000). Regenerate the file with
      // `npm run api:schema` (backend installed), or `python code/scripts/export_openapi.py`.
      target: "./openapi.json",
    },
    output: {
      mode: "tags-split",
      target: "./src/api/generated",
      client: "react-query",
      httpClient: "axios",
    },
  },
});
