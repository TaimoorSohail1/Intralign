"use client";

import { Bell, CaretDown, Check, FolderOpen, House, MagnifyingGlass, Plus, Sparkle, X } from "@phosphor-icons/react";
import Link from "next/link";
import { type KeyboardEvent as ReactKeyboardEvent, useEffect, useRef, useState } from "react";
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

function notificationDetail(notification: WorkspaceNotification) {
  if (notification.status === "failed") return "your last-good understanding is preserved";
  if (notification.kind === "review") return "attributed response received — analysis is updating";
  if (notification.kind === "mention") return "open the tied issue discussion";
  if (notification.kind === "extended") return "understanding refined — see History";
  return "the first read is ready";
}

export function ProjectWorkspaceControls({
  onOpenPlanSettings,
  planPortalId,
  projectId,
  projectName,
}: {
  onOpenPlanSettings?: () => void;
  planPortalId?: string;
  projectId: string;
  projectName?: string;
}) {
  const [workspace, setWorkspace] = useState<WorkspaceSummary | null>(null);
  const [open, setOpen] = useState(false);
  const [projectQuery, setProjectQuery] = useState("");
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [usageOpen, setUsageOpen] = useState(false);
  const [planPortalTarget, setPlanPortalTarget] = useState<HTMLElement | null>(null);
  const controlsRef = useRef<HTMLDivElement>(null);
  const notificationPanelRef = useRef<HTMLElement>(null);
  const switcherTriggerRef = useRef<HTMLButtonElement>(null);
  const switcherMenuRef = useRef<HTMLDivElement>(null);

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
      const target = event.target as Node;
      if (
        !controlsRef.current?.contains(target)
        && !notificationPanelRef.current?.contains(target)
      ) {
        setOpen(false);
        setNotificationsOpen(false);
      }
    };
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        const wasOpen = open;
        setOpen(false);
        setNotificationsOpen(false);
        if (wasOpen) switcherTriggerRef.current?.focus();
      }
    };
    document.addEventListener("mousedown", closeMenus);
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.removeEventListener("mousedown", closeMenus);
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, [open]);

  const projects = Array.from(new Map(
    (Array.isArray(workspace?.projects) ? workspace.projects : []).map((project) => [project.id, project]),
  ).values());
  const projectedActive = projects
    .filter((project) => !project.archived)
    .sort((left, right) => right.updated_at.localeCompare(left.updated_at));
  const active = projectedActive.some((project) => project.id === projectId)
    ? projectedActive
    : [{
      id: projectId,
      name: projectName ?? "Project",
      archived: false,
      analysis_status: "current",
      updated_at: "",
    } as WorkspaceSummary["projects"][number], ...projectedActive];
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
  const planLabel = workspace?.plan_label;

  const planControl = (
    <button
      aria-label={planLabel ?? "Loading plan"}
      aria-busy={!workspace}
      className="project-plan-badge"
      disabled={!workspace}
      onClick={() => {
        setOpen(false);
        setNotificationsOpen(false);
        if (!workspace) return;
        if (onOpenPlanSettings) onOpenPlanSettings();
        else setUsageOpen(true);
      }}
      title={workspace ? "Open Plan & usage settings" : "Loading plan"}
      type="button"
    >
      <Sparkle aria-hidden="true" size={14} weight="fill" />
      <span className="project-plan-copy">
        <strong>{workspace ? `${planLabel} plan` : "Loading plan"}</strong>
        <small>
          {workspace
            ? `${active.length} ${active.length === 1 ? "project" : "projects"} · people not capacity-gated`
            : "Loading workspace"}
        </small>
      </span>
      <em>Your plan</em>
    </button>
  );

  const handleSwitcherKeyDown = (event: ReactKeyboardEvent) => {
    if (!open) return;
    const items = Array.from(switcherMenuRef.current?.querySelectorAll<HTMLElement>('[role="menuitem"]') ?? []);
    if (!items.length) return;
    const currentIndex = items.indexOf(document.activeElement as HTMLElement);
    if (event.key === "ArrowDown" || event.key === "ArrowUp") {
      event.preventDefault();
      if (currentIndex < 0) {
        const currentProjectIndex = items.findIndex((item) => item.getAttribute("href")?.includes(projectId));
        items[Math.max(currentProjectIndex, 0)]?.focus();
        return;
      }
      const direction = event.key === "ArrowDown" ? 1 : -1;
      items[(currentIndex + direction + items.length) % items.length]?.focus();
    }
    if (event.key === "Home" || event.key === "End") {
      event.preventDefault();
      items[event.key === "Home" ? 0 : items.length - 1]?.focus();
    }
  };

  return (
    <div className="project-workspace-controls" ref={controlsRef}>
      <div className="project-switcher" onKeyDown={handleSwitcherKeyDown}>
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
          ref={switcherTriggerRef}
        >
          <FolderOpen aria-hidden="true" className="project-switcher-icon" size={15} />
          <span>{projectName ?? current?.name ?? "Project"}</span>
          <CaretDown aria-hidden="true" className="project-switcher-caret" size={13} />
        </button>
        {open ? (
          <div
            className="project-switcher-menu"
            ref={switcherMenuRef}
            role="menu"
          >
            <p>Projects</p>
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
            {workspace?.role === "owner" ? <Link href="/workspace?new=1" role="menuitem"><Plus size={15} /> New project</Link> : null}
            <Link href="/workspace" role="menuitem"><House size={15} /> Workspace Home</Link>
          </div>
        ) : null}
      </div>
      {workspace?.role === "owner" ? <ProjectCollaborationControls
          projectId={projectId}
          projectName={projectName ?? current?.name ?? "this project"}
        /> : null}
      {workspace?.role === "owner" && (planPortalId
        ? planPortalTarget
          ? createPortal(planControl, planPortalTarget)
          : null
        : planControl)}
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
        {notificationsOpen ? createPortal(
          <>
            <button aria-label="Close notifications" className="workspace-notification-scrim" onClick={() => setNotificationsOpen(false)} type="button" />
            <section aria-label="Notifications" aria-modal="true" className="workspace-notification-panel" ref={notificationPanelRef} role="dialog">
              <header>
                <div>
                  <strong>Notifications</strong>
                  <small>What moved — a durable record, not alerts.</small>
                </div>
                <div className="workspace-notification-actions">
                  <button aria-label="Close notifications" onClick={() => setNotificationsOpen(false)} type="button"><X size={17} /></button>
                </div>
              </header>
              <p className="workspace-notification-intro">
                A durable record, not alerts — routine changes never interrupt you; only miss-worthy ones surface. Self-acknowledged ones are skipped.
              </p>
              <div className="workspace-notification-list">
                {visibleNotifications.length ? visibleNotifications.map((notification) => (
                  <Link
                    className={notification.read ? "is-read" : "is-unread"}
                    href={notification.href ?? `/projects/${notification.project_id}/history`}
                    key={notification.key}
                  >
                    <div>
                      <small className="workspace-notification-time">{relativeTime(notification.created_at)}</small>
                      <p><strong>{notification.title}</strong> — {notificationDetail(notification)}.</p>
                    </div>
                  </Link>
                )) : <p>No notifications yet.</p>}
              </div>
            </section>
          </>,
          document.body,
        ) : null}
      </div>
      {workspace && !onOpenPlanSettings ? (
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
