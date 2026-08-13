"use client";

import {
  Archive,
  ArrowCounterClockwise,
  ArrowRight,
  Bell,
  FolderOpen,
  Gear,
  MagnifyingGlass,
  Plus,
  Sparkle,
} from "@phosphor-icons/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { PlanComparisonModal } from "@/components/workspace/plan-comparison-modal";
import type { WorkspaceSummary } from "@/lib/server/oslo-api";

const workspaceDateFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "2-digit",
  month: "short",
  timeZone: "UTC",
  year: "numeric",
});

export function WorkspaceHome({
  initial,
  displayName,
  openNewProject = false,
}: {
  initial: WorkspaceSummary;
  displayName: string;
  openNewProject?: boolean;
}) {
  const router = useRouter();
  const [workspace, setWorkspace] = useState(initial);
  const [showArchived, setShowArchived] = useState(false);
  const [pendingId, setPendingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [plansOpen, setPlansOpen] = useState(false);
  const [projectQuery, setProjectQuery] = useState("");
  const [visibleCount, setVisibleCount] = useState(12);
  const newProjectHandled = useRef(false);

  const active = useMemo(
    () => workspace.projects.filter((project) => !project.archived),
    [workspace.projects],
  );
  const archived = useMemo(
    () => workspace.projects.filter((project) => project.archived),
    [workspace.projects],
  );
  const activeSorted = useMemo(
    () => [...active].sort(
      (left, right) => Date.parse(right.updated_at) - Date.parse(left.updated_at),
    ),
    [active],
  );
  const activeFiltered = useMemo(() => {
    const query = projectQuery.trim().toLocaleLowerCase();
    return query
      ? activeSorted.filter((project) => project.name.toLocaleLowerCase().includes(query))
      : activeSorted;
  }, [activeSorted, projectQuery]);
  const activeVisible = activeFiltered.slice(0, visibleCount);
  const activeProjectLimit = workspace.active_project_limit ?? (workspace.plan === "free" ? 1 : 3);
  const canCreateProject = workspace.can_create_project ?? active.length < activeProjectLimit;
  const isReturningClient = workspace.projects.some(
    (project) => project.analysis_status !== "not_analyzed",
  );
  const intakeHref = useCallback(
    (projectId: string) =>
      `/intake?project=${projectId}${isReturningClient ? "&returning=1" : ""}`,
    [isReturningClient],
  );
  const activeProjectLimitMessage =
    `The ${workspace.plan_label} plan includes ${activeProjectLimit} active project${activeProjectLimit === 1 ? "" : "s"}. Archive one or compare plans.`;

  const createProject = async () => {
    setError(null);
    if (!canCreateProject) {
      setError(activeProjectLimitMessage);
      setPlansOpen(true);
      return;
    }
    const response = await fetch("/api/projects/new", { method: "POST" });
    if (!response.ok) {
      setError("The project could not be created. Please try again.");
      return;
    }
    const project = await response.json();
    router.push(intakeHref(project.id));
  };

  useEffect(() => {
    if (
      !openNewProject
      || newProjectHandled.current
    ) return;

    newProjectHandled.current = true;
    let cancelled = false;
    if (!canCreateProject) {
      queueMicrotask(() => {
        if (cancelled) return;
        setError(activeProjectLimitMessage);
        setPlansOpen(true);
      });
      return () => {
        cancelled = true;
      };
    }
    void fetch("/api/projects/new", { method: "POST" }).then(async (response) => {
      if (cancelled) return;
      if (!response.ok) {
        setError("The project could not be created. Please try again.");
        return;
      }
      const project = await response.json();
      router.push(intakeHref(project.id));
    });
    return () => {
      cancelled = true;
    };
  }, [activeProjectLimitMessage, canCreateProject, intakeHref, openNewProject, router]);

  const setArchived = async (
    projectId: string,
    next: boolean,
  ) => {
    setPendingId(projectId);
    setError(null);
    const response = await fetch(
      `/api/workspace/projects/${projectId}/${next ? "archive" : "restore"}`,
      { method: "POST" },
    );
    if (!response.ok) {
      setError(`The project could not be ${next ? "archived" : "restored"}.`);
      setPendingId(null);
      return;
    }
    setWorkspace((current) => {
      const projects = current.projects.map((project) =>
        project.id === projectId ? { ...project, archived: next } : project,
      );
      const activeProjectCount = projects.filter((project) => !project.archived).length;
      return {
        ...current,
        projects,
        can_create_project: activeProjectCount < activeProjectLimit,
      };
    });
    setPendingId(null);
    return true;
  };

  return (
    <main className="workspace-home-shell">
      <header className="workspace-home-header">
        <Link className="workspace-home-brand" href="/workspace">
          <span aria-hidden="true">I</span>
          <strong>Intralign</strong>
        </Link>
        <div className="workspace-home-actions">
          <Link aria-label="Notifications" href="/workspace#activity">
            <Bell size={18} />
          </Link>
          <Link aria-label="Settings" href="/settings">
            <Gear size={18} />
          </Link>
          <span className="workspace-avatar" title={displayName}>
            {displayName.slice(0, 1).toUpperCase()}
          </span>
        </div>
      </header>

      <section className="workspace-home-content">
        <div className="workspace-home-title">
          <div>
            <p>Workspace</p>
            <h1>{workspace.name}</h1>
            <span>Open a project or start a new strategic read.</span>
          </div>
          <div className="workspace-create-control">
            <small>{active.length} active · {activeProjectLimit} included</small>
            <button
              className="workspace-primary-action"
              onClick={createProject}
              type="button"
            >
              <Plus size={16} weight="bold" />
              New project
            </button>
          </div>
        </div>

        <section className="workspace-plan-strip" aria-label="Workspace plan">
          <div className="workspace-plan-summary">
            <Sparkle size={18} />
            <div>
              <strong>{workspace.plan_label} plan</strong>
              <span>{activeProjectLimit} active project{activeProjectLimit === 1 ? "" : "s"}</span>
            </div>
          </div>
          <button onClick={() => setPlansOpen(true)} type="button">
            Compare plans <ArrowRight size={14} />
          </button>
        </section>

        <aside className="workspace-score-note">
          <span>i</span>
          <p>
            <strong>Each project keeps its own evidence-qualified read.</strong>
            No computed scores across projects — OSLO assesses each project on its own inputs and reliability.
            There is no portfolio score, average, or ranking.
          </p>
        </aside>

        {error ? <p className="workspace-error" role="alert">{error}</p> : null}

        <div className="workspace-section-heading">
          <div>
            <h2>Active projects</h2>
            <span>{active.length}</span>
          </div>
          <label className="workspace-project-search">
            <MagnifyingGlass aria-hidden="true" size={15} />
            <span className="sr-only">Search active projects</span>
            <input
              onChange={(event) => {
                setProjectQuery(event.target.value);
                setVisibleCount(12);
              }}
              placeholder="Search projects"
              type="search"
              value={projectQuery}
            />
          </label>
        </div>

        <div className={`workspace-project-grid ${activeVisible.length === 1 ? "is-single" : ""}`}>
          {activeVisible.map((project) => (
            <article className="workspace-project-card" key={project.id}>
              <div className="workspace-project-card-top">
                <span className={`workspace-state workspace-state-${project.analysis_status}`}>
                  {project.analysis_status.replace("_", " ")}
                </span>
                {workspace.role === "owner" ? (
                  <button
                    aria-label={`Archive ${project.name}`}
                    disabled={pendingId === project.id}
                    onClick={() => setArchived(project.id, true)}
                    type="button"
                  >
                    <Archive size={16} />
                  </button>
                ) : null}
              </div>
              <div className="workspace-project-identity">
                <span>{activeVisible.length === 1 ? "Your project" : "Project"}</span>
                <h3>{project.name}</h3>
                <p>
                  {project.confidence_band
                    ? `${project.confidence_band} understanding · ${project.reliability} reliability`
                    : "Ready for project intake"}
                </p>
              </div>
              <dl>
                <div><dt>Issues</dt><dd>{project.open_issues} open</dd></div>
                <div><dt>Artifacts</dt><dd>{project.artifact_count} / 7</dd></div>
                <div>
                  <dt>Updated</dt>
                  <dd>{workspaceDateFormatter.format(new Date(project.updated_at))}</dd>
                </div>
              </dl>
              <Link href={
                project.analysis_status === "not_analyzed"
                  ? intakeHref(project.id)
                  : `/projects/${project.id}/overview`
              }>
                Open project <ArrowRight size={15} />
              </Link>
            </article>
          ))}
          {active.length === 0 ? (
            <button className="workspace-empty-card" onClick={createProject} type="button">
              <FolderOpen size={28} />
              <strong>Create your first project</strong>
              <span>Describe a plan or upload evidence to begin.</span>
            </button>
          ) : null}
        </div>
        {activeFiltered.length === 0 && active.length > 0 ? (
          <div className="workspace-no-results">
            <MagnifyingGlass size={22} />
            <strong>No matching projects</strong>
            <span>Try a different project name.</span>
          </div>
        ) : null}
        {activeVisible.length < activeFiltered.length ? (
          <div className="workspace-load-more">
            <span>Showing {activeVisible.length} of {activeFiltered.length} projects</span>
            <button onClick={() => setVisibleCount((count) => count + 12)} type="button">
              Show more
            </button>
          </div>
        ) : null}

        <section className="workspace-archived">
          <button
            aria-expanded={showArchived}
            onClick={() => setShowArchived((current) => !current)}
            type="button"
          >
            <Archive size={16} />
            Archived projects
            <span>{archived.length}</span>
          </button>
          {showArchived ? (
            <div>
              {archived.length ? archived.map((project) => (
                <article key={project.id}>
                  <div><strong>{project.name}</strong><span>Read-only · retained safely</span></div>
                  {workspace.role === "owner" ? (
                    <button
                      disabled={pendingId === project.id}
                      onClick={() => setArchived(project.id, false)}
                      type="button"
                    >
                      <ArrowCounterClockwise size={15} /> Restore
                    </button>
                  ) : null}
                </article>
              )) : <p>No archived projects.</p>}
            </div>
          ) : null}
        </section>

        <section className="workspace-activity" id="activity">
          <div className="workspace-section-heading">
            <div><h2>Recent activity</h2></div>
            <p>Project-aware, non-mutating updates.</p>
          </div>
          {workspace.notifications.slice(0, 5).map((notification) => (
            <Link href={`/projects/${notification.project_id}/history`} key={notification.key}>
              <span className={`workspace-activity-dot ${notification.status === "failed" ? "is-failed" : ""}`} />
              <div>
                <strong>{notification.project_name}</strong>
                <span>{notification.title}</span>
              </div>
              <ArrowRight size={15} />
            </Link>
          ))}
          {!workspace.notifications.length ? <p>No analysis activity yet.</p> : null}
        </section>
      </section>

      <PlanComparisonModal
        onClose={() => setPlansOpen(false)}
        onWorkspaceChange={setWorkspace}
        open={plansOpen}
        workspace={workspace}
      />
    </main>
  );
}
