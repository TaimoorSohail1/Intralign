"use client";

import { Bell, CaretDown, Check, DotsThree, FolderOpen, House, MagnifyingGlass, Plus, Sparkle, WarningCircle, X } from "@phosphor-icons/react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";

import { ProjectCollaborationControls } from "@/components/collaboration/project-collaboration-controls";
import { UsageLimitsModal } from "@/components/workspace/usage-limits-modal";
import type { WorkspaceSummary } from "@/lib/server/oslo-api";

type WorkspaceNotification = WorkspaceSummary["notifications"][number];

function uniqueNotifications(notifications: WorkspaceNotification[]) {
  const byKey = new Map<string, WorkspaceNotification>();
  for (const notification of notifications) {
    if (!byKey.has(notification.key)) byKey.set(notification.key, notification);
  }
  return Array.from(byKey.values());
}

function notificationProjectLabel(notification: WorkspaceNotification) {
  if (notification.project_name !== "Untitled project") return notification.project_name;
  return `${notification.project_name} · ${notification.project_id.slice(0, 8)}`;
}

function relativeTime(value: string) {
  const timestamp = new Date(value).getTime();
  if (Number.isNaN(timestamp)) return value;
  const minutes = Math.floor(Math.max(Date.now() - timestamp, 0) / 60_000);
  if (minutes < 1) return "just now";
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  return `${Math.floor(hours / 24)}d ago`;
}

export function ProjectWorkspaceControls({
  planPortalId,
  projectId,
}: {
  planPortalId?: string;
  projectId: string;
}) {
  const [workspace, setWorkspace] = useState<WorkspaceSummary | null>(null);
  const [open, setOpen] = useState(false);
  const [projectQuery, setProjectQuery] = useState("");
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [usageOpen, setUsageOpen] = useState(false);
  const [markingRead, setMarkingRead] = useState(false);
  const [planPortalTarget, setPlanPortalTarget] = useState<HTMLElement | null>(null);
  const controlsRef = useRef<HTMLDivElement>(null);

  const updateNow = async () => {
    const response = await fetch(`/api/projects/${projectId}/analysis-runs/refresh`, {
      method: "POST",
    });
    const body = await response.json().catch(() => null);
    if (!response.ok || !body?.run_id) {
      throw new Error(body?.message ?? "Analysis could not refresh");
    }
    window.location.assign(`/projects/${projectId}/analysis/${body.run_id}`);
  };

  useEffect(() => {
    const frame = window.requestAnimationFrame(() => {
      setPlanPortalTarget(
        planPortalId ? document.getElementById(planPortalId) : null,
      );
    });
    return () => window.cancelAnimationFrame(frame);
  }, [planPortalId]);

  useEffect(() => {
    let cancelled = false;
    void (async () => {
      try {
        const response = await fetch("/api/workspace", { cache: "no-store" });
        if (!response?.ok || cancelled) return;
        const value = await response.json();
        if (
          !cancelled
          && value
          && Array.isArray(value.projects)
          && Array.isArray(value.notifications)
        ) {
          setWorkspace(value);
        }
      } catch {
        // Workspace awareness is an enhancement; the project must remain usable
        // if its background request is unavailable.
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    const closeMenus = (event: MouseEvent) => {
      if (!controlsRef.current?.contains(event.target as Node)) {
        setOpen(false);
        setNotificationsOpen(false);
      }
    };
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        setOpen(false);
        setNotificationsOpen(false);
      }
    };
    document.addEventListener("mousedown", closeMenus);
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.removeEventListener("mousedown", closeMenus);
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, []);

  const projects = Array.isArray(workspace?.projects) ? workspace.projects : [];
  const active = projects
    .filter((project) => !project.archived)
    .sort((left, right) => right.updated_at.localeCompare(left.updated_at));
  const current = active.find((project) => project.id === projectId);
  const normalizedProjectQuery = projectQuery.trim().toLowerCase();
  const matchingProjects = normalizedProjectQuery
    ? active.filter((project) => project.name.toLowerCase().includes(normalizedProjectQuery))
    : active;
  const visibleProjects = matchingProjects.slice(0, 8);
  const notifications = uniqueNotifications(
    Array.isArray(workspace?.notifications) ? workspace.notifications : [],
  );
  const unread = notifications.filter((notification) => !notification.read);
  const visibleNotifications = notifications.slice(0, 8);
  const planLabel = workspace?.plan_label ?? "Free";

  const planControl = (
    <button
      aria-label={planLabel}
      aria-busy={!workspace}
      className="project-plan-badge"
      onClick={() => {
        setOpen(false);
        setNotificationsOpen(false);
        if (workspace) setUsageOpen(true);
      }}
      title={workspace ? "View usage and limits" : "Loading plan"}
      type="button"
    >
      <Sparkle aria-hidden="true" size={14} weight="fill" />
      <span className="project-plan-copy">
        <strong>{planLabel} plan</strong>
        <small>
          {active.length} {active.length === 1 ? "project" : "projects"}
          {workspace ? ` · ${workspace.collaborator_seat_limit} seats` : ""}
          {workspace?.plan === "free" ? " · 2 invites/mo" : ""}
        </small>
      </span>
      <em>Your plan</em>
    </button>
  );

  const markAllRead = async () => {
    if (!unread.length) return;
    setMarkingRead(true);
    const response = await fetch("/api/workspace/notifications/read", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ keys: unread.map((notification) => notification.key) }),
    });
    if (response.ok) {
      setWorkspace((currentWorkspace) => currentWorkspace ? {
        ...currentWorkspace,
        notifications: (currentWorkspace.notifications ?? []).map((notification) => ({
          ...notification,
          read: true,
        })),
      } : currentWorkspace);
    }
    setMarkingRead(false);
  };

  return (
    <div className="project-workspace-controls" ref={controlsRef}>
      <div className="project-switcher">
        <button
          aria-expanded={open}
          aria-haspopup="menu"
          className="project-switcher-trigger"
          onClick={() => {
            setNotificationsOpen(false);
            setOpen((value) => !value);
          }}
          title="Switch project"
          type="button"
        >
          <FolderOpen aria-hidden="true" className="project-switcher-icon" size={15} />
          <span>{current?.name ?? "Project"}</span>
          <CaretDown aria-hidden="true" className="project-switcher-caret" size={13} />
        </button>
        {open ? (
          <div className="project-switcher-menu" role="menu">
            <p>{workspace?.name ?? "Workspace"}</p>
            <Link href="/workspace" role="menuitem"><House size={15} /> Workspace Home</Link>
            <div className="project-switcher-divider" />
            {active.length > 5 ? (
              <label className="project-switcher-search">
                <MagnifyingGlass aria-hidden="true" size={14} />
                <span className="sr-only">Find a project</span>
                <input
                  aria-label="Find a project"
                  onChange={(event) => setProjectQuery(event.target.value)}
                  placeholder="Find a project"
                  value={projectQuery}
                />
              </label>
            ) : null}
            <div className="project-switcher-projects">
            {visibleProjects.map((project) => (
              <Link href={project.analysis_status === "not_analyzed" ? `/intake?project=${project.id}` : `/projects/${project.id}/overview`} key={project.id} role="menuitem">
                {project.id === projectId ? <Check size={14} /> : <span />}
                <div><strong>{project.name}</strong><small>{project.analysis_status.replace("_", " ")}</small></div>
              </Link>
            ))}
            {!visibleProjects.length ? <p className="project-switcher-empty">No matching projects</p> : null}
            </div>
            {matchingProjects.length > visibleProjects.length ? (
              <Link className="project-switcher-view-all" href="/workspace" role="menuitem">
                View all {active.length} projects
              </Link>
            ) : null}
            <div className="project-switcher-divider" />
            <Link href="/workspace?new=1" role="menuitem"><Plus size={15} /> New project</Link>
          </div>
        ) : null}
      </div>
      <ProjectCollaborationControls projectId={projectId} projectName={current?.name ?? "this project"} />
      {planPortalId
        ? planPortalTarget
          ? createPortal(planControl, planPortalTarget)
          : null
        : planControl}
      <div className="workspace-notifications">
        <button
          aria-expanded={notificationsOpen}
          aria-label="Notifications"
          onClick={() => {
            setOpen(false);
            setNotificationsOpen((value) => !value);
          }}
          title="Notifications"
          type="button"
        >
          <Bell size={16} />{unread.length ? <i>{unread.length}</i> : null}
        </button>
        {notificationsOpen ? (
          <>
            <button aria-label="Close notifications" className="workspace-notification-scrim" onClick={() => setNotificationsOpen(false)} type="button" />
            <section aria-label="Notifications" aria-modal="true" className="workspace-notification-panel" role="dialog">
              <header>
                <div>
                  <strong>Notifications</strong>
                  <small>awareness</small>
                </div>
                <div className="workspace-notification-actions">
                  <button aria-label="Close notifications" onClick={() => setNotificationsOpen(false)} type="button"><X size={17} /></button>
                </div>
              </header>
              <div className="workspace-notification-tools">
                <button disabled={!unread.length || markingRead} onClick={markAllRead} type="button">Mark all read</button>
                <span>{unread.length} unread</span>
              </div>
              <div className="workspace-notification-list">
                {visibleNotifications.length ? visibleNotifications.map((notification) => (
                  <Link
                    className={notification.read ? "is-read" : "is-unread"}
                    href={`/projects/${notification.project_id}/history`}
                    key={notification.key}
                  >
                    <span className={`workspace-activity-dot ${notification.status === "failed" ? "is-failed" : ""}`} />
                    <span className="workspace-notification-icon">
                      {notification.status === "failed" ? <WarningCircle size={15} /> : notification.kind === "extended" ? <Check size={15} /> : <DotsThree size={15} />}
                    </span>
                    <div>
                      <p><strong>{notification.title}</strong><span>{notificationProjectLabel(notification)} · {notification.status === "failed" ? "your last-good understanding is preserved" : notification.kind === "extended" ? "understanding refined — see History" : "the first read is ready"}</span></p>
                      <small>{relativeTime(notification.created_at)} <i>{notification.status === "failed" ? "analysis failed" : "analysis complete"}</i></small>
                    </div>
                  </Link>
                )) : <p>No notifications yet.</p>}
              </div>
              <footer>
                <p><strong>Awareness only.</strong> Notifications never start analysis, and marking them read changes nothing in your project.</p>
              </footer>
            </section>
          </>
        ) : null}
      </div>
      {workspace ? (
        <UsageLimitsModal
          onClose={() => setUsageOpen(false)}
          onUpdate={updateNow}
          open={usageOpen}
          workspace={workspace}
        />
      ) : null}
    </div>
  );
}
