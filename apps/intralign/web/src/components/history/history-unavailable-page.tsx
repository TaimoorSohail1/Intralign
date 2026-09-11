import Link from "next/link";

export function HistoryUnavailablePage({ projectId }: { projectId: string }) {
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
      <div className="project-grid is-panel-closed">
        <section className="project-main">
          <div className="failure-card" role="status">
            <strong>Project History is temporarily unavailable.</strong>
            <span>
              Your project data is unchanged. Try again shortly, or return to your workspace.
            </span>
            <p>
              <Link href={`/projects/${projectId}/history`}>Try History again</Link>
              {" · "}
              <Link href="/workspace">Return to workspace</Link>
            </p>
          </div>
        </section>
      </div>
    </main>
  );
}
