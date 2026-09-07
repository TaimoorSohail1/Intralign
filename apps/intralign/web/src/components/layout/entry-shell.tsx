import type { PropsWithChildren } from "react";

import { BrandLockup } from "@/components/brand/brand-lockup";
import { shortBuildIdentity } from "@/lib/build-identity";

export function EntryShell({ children }: PropsWithChildren) {
  return (
    <main className="entry-shell">
      <BrandLockup />
      {children}
      <footer className="entry-footer">
        ⓘ OSLO advises; you decide — you stay in control at every step.
        <span className="entry-build">Build {shortBuildIdentity()}</span>
      </footer>
    </main>
  );
}
