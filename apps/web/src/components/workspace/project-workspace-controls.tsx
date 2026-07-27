"use client";

import { Bell, CaretDown, Check, FolderOpen, Gear, House, MagnifyingGlass, Plus, X } from "@phosphor-icons/react";
import Link from "next/link";
import { useEffect, useRef, useState } from "react";

import { ProjectCollaborationControls } from "@/components/collaboration/project-collaboration-controls";
import type { WorkspaceSummary } from "@/lib/server/oslo-api";

export function ProjectWorkspaceControls({ projectId }: { projectId: string }) {
  const [workspace, setWorkspace] = useState<WorkspaceSummary | null>(null);
  const [open, setOpen] = useState(false);
  const [projectQuery, setProjectQuery] = useState("");
  const [notificationsOpen, setNotificationsOpen] = useState(false);
  const [markingRead, setMarkingRead] = useState(false);
  const controlsRef = useRef<HTMLDivElement>(null);

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
  const notifications = Array.isArray(workspace?.notifications) ? workspace.notifications : [];
  const unread = notifications.filter((notification) => !notification.read);
  const visibleNotifications = notifications.slice(0, 8);

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
      <ProjectCollaborationControls projectId={projectId} />
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
                  <span>Workspace awareness</span>
                  <strong>Notifications</strong>
                  <small>{unread.length} unread</small>
                </div>
                <div className="workspace-notification-actions">
                  <button disabled={!unread.length || markingRead} onClick={markAllRead} type="button">Mark all read</button>
                  <Link aria-label="Notification settings" href="/settings#notifications"><Gear size={17} /></Link>
                  <button aria-label="Close notifications" onClick={() => setNotificationsOpen(false)} type="button"><X size={17} /></button>
                </div>
              </header>
              <div className="workspace-notification-list">
                {visibleNotifications.length ? visibleNotifications.map((notification) => (
                  <Link
                    className={notification.read ? "is-read" : ""}
                    href={`/projects/${notification.project_id}/history`}
                    key={notification.key}
                  >
                    <span className={`workspace-activity-dot ${notification.status === "failed" ? "is-failed" : ""}`} />
                    <div>
                      <small>{notification.project_name}</small>
                      <strong>{notification.title}</strong>
                      <span>Open retained history <span aria-hidden="true">→</span></span>
                    </div>
                  </Link>
                )) : <p>No notifications yet.</p>}
              </div>
              <footer>
                <p><strong>Awareness only.</strong> Opening, reading, or marking a notification never starts analysis.</p>
                <Link className="workspace-notification-footer" href="/workspace#activity">View workspace activity</Link>
              </footer>
            </section>
          </>
        ) : null}
      </div>
    </div>
  );
}
