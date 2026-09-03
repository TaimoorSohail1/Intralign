import Link from "next/link";

import { HistoryWorkspace } from "@/components/history/history-workspace";
import type { ProjectHistory } from "@/lib/server/oslo-api";

export function HistoryOnlyPage({
  history,
  projectId,
}: {
  history: ProjectHistory;
  projectId: string;
}) {
  return (
    <main className="project-shell">
      <header className="project-header">
        <Link className="project-toolbar-brand" href="/workspace">
          <span aria-hidden="true">I</span>
          <strong>Intralign</strong>
        </Link>
        <div className="project-context">
          <strong>Project activity</strong>
          <span aria-hidden="true">›</span>
          <em>History</em>
        </div>
      </header>
      <aside className="workspace-sidebar">
        <p className="workspace-label">Project</p>
        <nav aria-label="Workspace">
          <Link href={`/intake?project=${projectId}`}>Analysis</Link>
          <Link aria-current="page" className="is-current" href={`/projects/${projectId}/history`}>
            History
          </Link>
          <Link href="/workspace">All projects</Link>
        </nav>
        <div className="workspace-sidebar-footer">
          <span>OSLO advises; you decide.</span>
        </div>
      </aside>
      <div className="project-grid is-panel-closed">
        <section className="project-main">
          <div className="failure-card" role="status">
            <strong>No trusted project read is available yet.</strong>
            <span>
              Analysis activity and failures remain available below. Retry from
              Analysis when you are ready.
            </span>
          </div>
          <HistoryWorkspace history={history} projectId={projectId} />
        </section>
      </div>
    </main>
  );
}
