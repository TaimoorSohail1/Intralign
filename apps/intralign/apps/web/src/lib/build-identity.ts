const BUILD_IDENTITY_VARIABLES = [
  "NEXT_PUBLIC_BUILD_SHA",
  "VERCEL_GIT_COMMIT_SHA",
  "HEROKU_SLUG_COMMIT",
  "SOURCE_VERSION",
] as const;

/**
 * Resolve the running build to its source commit.
 *
 * Criterion N-5: a measurement can only be attributed to a build when a surface
 * names the commit it was taken from. Returns "unknown" rather than guessing,
 * so an unstamped deploy is visible instead of silently plausible.
 */
export function buildIdentity(): string {
  for (const variable of BUILD_IDENTITY_VARIABLES) {
    const commit = process.env[variable]?.trim();
    if (commit) {
      return commit;
    }
  }
  return "unknown";
}

/** The short form shown to a reader; full commit stays on `<html data-build>`. */
export function shortBuildIdentity(): string {
  const commit = buildIdentity();
  return commit === "unknown" ? commit : commit.slice(0, 7);
}
