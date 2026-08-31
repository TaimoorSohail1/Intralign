import type { PropsWithChildren } from "react";

import { BrandLockup } from "@/components/brand/brand-lockup";

export function EntryShell({ children }: PropsWithChildren) {
  return (
    <main className="entry-shell">
      <BrandLockup />
      {children}
      <footer className="entry-footer">ⓘ OSLO advises; you decide — you stay in control at every step.</footer>
    </main>
  );
}
