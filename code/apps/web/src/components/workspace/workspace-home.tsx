"use client";

import { Archive, ArrowCounterClockwise, ArrowRight, Plus } from "@phosphor-icons/react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";

import { PlanComparisonModal } from "@/components/workspace/plan-comparison-modal";
import { ProjectCapacityModal } from "@/components/workspace/project-capacity-modal";
import type { WorkspaceSummary } from "@/lib/server/oslo-api";

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
  const [pendingId, setPendingId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [plansOpen, setPlansOpen] = useState(false);
  const [capacityOpen, setCapacityOpen] = useState(false);
  const [creatingProject, setCreatingProject] = useState(false);
  const newProjectHandled = useRef(false);
  const projectCreationPending = useRef(false);

  const projects = useMemo(
    () => Array.from(new Map(workspace.projects.map((project) => [project.id, project])).values()),
    [workspace.projects],
  );
  const active = useMemo(
    () => projects
      .filter((project) => !project.archived)
      .sort((left, right) => Date.parse(right.updated_at) - Date.parse(left.updated_at)),
    [projects],
  );
  const archived = useMemo(
    () => projects.filter((project) => project.archived),
    [projects],
  );
  const currentProject = active[0] ?? null;
  const recentProjects = active.slice(1);
  const activeProjectLimit = workspace.active_project_limit ?? (workspace.plan === "free" ? 1 : 3);
  const isReturningClient = workspace.projects.some(
    (project) => project.analysis_status !== "not_analyzed",
  );
  const intakeHref = useCallback(
    (projectId: string) => `/intake?project=${projectId}${isReturningClient ? "&returning=1" : ""}`,
    [isReturningClient],
  );
  const activeProjectLimitMessage =
    `The ${workspace.plan_label} plan includes ${activeProjectLimit} active project${activeProjectLimit === 1 ? "" : "s"}. Archive one or compare plans.`;

  const createProject = useCallback(async () => {
    if (projectCreationPending.current) return;
    projectCreationPending.current = true;
    setCreatingProject(true);
    setError(null);
    try {
      const response = await fetch("/api/projects/new", { method: "POST" });
      if (!response.ok) {
        if (response.status === 422) {
          setError(activeProjectLimitMessage);
          setCapacityOpen(true);
        } else {
          setError("The project could not be created. Please try again.");
        }
        projectCreationPending.current = false;
        setCreatingProject(false);
        return;
      }
      const project = await response.json();
      router.push(intakeHref(project.id));
    } catch {
      setError("The project could not be created. Please try again.");
      projectCreationPending.current = false;
      setCreatingProject(false);
    }
  }, [activeProjectLimitMessage, intakeHref, router]);

  useEffect(() => {
    if (!openNewProject || newProjectHandled.current) return;
    newProjectHandled.current = true;
    window.history.replaceState(window.history.state, "", "/workspace");
    void createProject();
  }, [createProject, openNewProject]);

  const setArchived = async (projectId: string, next: boolean) => {
    setPendingId(projectId);
    setError(null);
    try {
      const response = await fetch(
        `/api/workspace/projects/${projectId}/${next ? "archive" : "restore"}`,
        { method: "POST" },
      );
      if (!response.ok) {
        setError(`The project could not be ${next ? "archived" : "restored"}.`);
        return false;
      }
      setWorkspace((current) => {
        const projects = current.projects.map((project) =>
          project.id === projectId ? { ...project, archived: next } : project,
        );
        return {
          ...current,
          projects,
          can_create_project: projects.filter((project) => !project.archived).length < activeProjectLimit,
        };
      });
      return true;
    } catch {
      setError(`The project could not be ${next ? "archived" : "restored"}.`);
      return false;
    } finally {
      setPendingId(null);
    }
  };

  const archiveAndCreate = async () => {
    if (!currentProject) return;
    const archivedCurrent = await setArchived(currentProject.id, true);
    if (!archivedCurrent) return;
    setCapacityOpen(false);
    await createProject();
  };

  const projectHref = (project: WorkspaceSummary["projects"][number]) =>
    project.analysis_status === "not_analyzed"
      ? intakeHref(project.id)
      : `/projects/${project.id}/overview`;

  return (
    <main aria-label={`${displayName}'s workspace`} className="r2-plans-shell">
      <section className="r2-plans-content">
        <header className="r2-plans-heading">
          <div><h1>Your project</h1><p>Pick up where understanding stands.</p></div>
          <button aria-label="New project" disabled={creatingProject} onClick={() => void createProject()} type="button">
            <Plus aria-hidden="true" size={14} /> New project
          </button>
        </header>

        {error && !capacityOpen ? <p className="workspace-error" role="alert">{error}</p> : null}

        <p className="r2-plans-label">Your project</p>
        <div className="r2-plans-primary-grid">
          {currentProject ? (
            <article className="r2-current-plan">
              <header>
                <h2>{currentProject.name}</h2>
                <span>{currentProject.analysis_status.replaceAll("_", " ")} · plan</span>
              </header>
              <p className="r2-plan-integrity">
                <i aria-hidden="true" /> Outcome Integrity
                <strong>{currentProject.confidence_band ?? "Not read"}</strong>
                <span>· gated by its weakest pillar</span>
              </p>
              <p className="r2-plan-updated">
                {currentProject.analysis_status === "not_analyzed" ? "Ready for intake" : "Analyzed"} · {currentProject.open_issues} open issues · {currentProject.artifact_count} artifacts
              </p>
              <dl>
                <div><dt>Outcome Integrity</dt><dd>{currentProject.confidence_band ?? "Not read"}</dd></div>
                <div><dt>Weakest pillar</dt><dd>{currentProject.weakest_pillar ?? "Not read"}</dd></div>
                <div><dt>Open issues</dt><dd>{currentProject.open_issues}</dd></div>
                <div><dt>Plan artifacts</dt><dd>{currentProject.artifact_count}</dd></div>
              </dl>
              <footer>
                <div><span>Owned</span><span>★ Pinned</span></div>
                {workspace.role === "owner" ? (
                  <button
                    aria-label={`Archive ${currentProject.name}`}
                    disabled={pendingId === currentProject.id}
                    onClick={() => void setArchived(currentProject.id, true)}
                    title="Archive project"
                    type="button"
                  ><Archive size={14} /></button>
                ) : null}
                <Link href={projectHref(currentProject)}>Open the project <ArrowRight size={14} /></Link>
              </footer>
            </article>
          ) : (
            <button className="r2-current-plan is-empty" disabled={creatingProject} onClick={() => void createProject()} type="button">
              <Plus size={19} /><strong>Create your first plan</strong><span>Drop in a document with context.</span>
            </button>
          )}

          {currentProject ? (
            <button aria-label="Create a new project" className="r2-new-plan" disabled={creatingProject} onClick={() => void createProject()} type="button">
              <Plus aria-hidden="true" size={19} />
              <strong>New project</strong>
              <span>Drop any document with context — OSLO maps it.</span>
            </button>
          ) : null}
        </div>

        <section className="r2-plans-list" aria-labelledby="recent-plans">
          <h2 id="recent-plans">Recent</h2>
          {recentProjects.length ? recentProjects.map((project) => (
            <article key={project.id}>
              <Link href={projectHref(project)}>
                <strong>{project.name}</strong>
                <span>{project.analysis_status.replaceAll("_", " ")} · integrity {project.confidence_band ?? "not read"}</span>
                <em>switch →</em>
              </Link>
            </article>
          )) : <p>No other recent plans.</p>}
        </section>

        <section className="r2-plans-list is-archived" aria-labelledby="archived-plans">
          <h2 id="archived-plans">Archived ({archived.length})</h2>
          {archived.length ? archived.map((project) => (
            <article key={project.id}>
              <div>
                <strong>{project.name}</strong><span>Read-only · retained safely</span>
                {workspace.role === "owner" ? (
                  <button disabled={pendingId === project.id} onClick={() => void setArchived(project.id, false)} type="button">
                    <ArrowCounterClockwise size={14} /> Restore
                  </button>
                ) : null}
              </div>
            </article>
          )) : <p>No archived plans.</p>}
        </section>

        <aside className="r2-portfolio-note">
          <strong>No portfolio score across plans.</strong> OSLO assesses each plan on its own inputs and grounding — there is no average, ranking, or roll-up score.
        </aside>
      </section>

      <PlanComparisonModal
        onClose={() => setPlansOpen(false)}
        onWorkspaceChange={setWorkspace}
        open={plansOpen}
        workspace={workspace}
      />
      <ProjectCapacityModal
        busy={pendingId !== null || creatingProject}
        currentProjectName={currentProject?.name ?? "your current project"}
        onArchive={() => void archiveAndCreate()}
        onClose={() => setCapacityOpen(false)}
        onComparePlans={() => {
          setCapacityOpen(false);
          setPlansOpen(true);
        }}
        open={capacityOpen}
        planLabel={workspace.plan_label}
      />
    </main>
  );
}
