"use client";

import {
  ArrowLeft,
  Bell,
  Buildings,
  Check,
  CreditCard,
  Desktop,
  Gear,
  Key,
  LinkSimple,
  MagnifyingGlass,
  Moon,
  SignOut,
  SlidersHorizontal,
  Sun,
  Trash,
  User,
  Users,
  X,
} from "@phosphor-icons/react";
import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";

import { PlanComparisonModal } from "@/components/workspace/plan-comparison-modal";
import type { WorkspacePreferences, WorkspaceSummary } from "@/lib/server/oslo-api";

const settingsSections = [
  { id: "account", label: "Account", group: "You", Icon: User },
  { id: "profile", label: "Profile", group: "You", Icon: User },
  { id: "appearance", label: "Appearance", group: "You", Icon: Sun },
  { id: "notifications", label: "Notifications", group: "You", Icon: Bell },
  { id: "workspace", label: "Workspace", group: "Workspace", Icon: Buildings },
  { id: "project-defaults", label: "Project defaults", group: "Workspace", Icon: SlidersHorizontal },
  { id: "collaboration", label: "Collaboration", group: "Workspace", Icon: Users },
  { id: "access", label: "Access & invites", group: "Workspace", Icon: Key },
  { id: "membership", label: "Membership", group: "Workspace", Icon: Users, badge: "View" },
  { id: "subscription", label: "Subscription", group: "Plan", Icon: CreditCard, badge: "View" },
  { id: "billing", label: "Billing", group: "Plan", Icon: CreditCard, badge: "View" },
  { id: "integrations", label: "Integrations", group: "Plan", Icon: LinkSimple, badge: "Later" },
] as const;

const collaborationNotifications = [
  ["Mentions", "when someone mentions you"],
  ["Replies", "when someone replies to you"],
  ["Shared with me", "when a project is shared with you"],
] as const;

export function WorkspaceSettings({
  initial,
  workspaceName,
  displayName,
  email,
  logoutAction,
  workspace,
}: {
  initial: WorkspacePreferences;
  workspaceName: string;
  displayName: string;
  email?: string;
  logoutAction?: () => Promise<void>;
  workspace?: WorkspaceSummary;
}) {
  const [preferences, setPreferences] = useState(initial);
  const [saved, setSaved] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const saveQueueRef = useRef<Promise<void>>(Promise.resolve());
  const saveRevisionRef = useRef(0);
  const [query, setQuery] = useState("");
  const [deleteOpen, setDeleteOpen] = useState(false);
  const [localDisplayName, setLocalDisplayName] = useState(
    initial.display_name || displayName,
  );
  const [localWorkspaceName, setLocalWorkspaceName] = useState(
    initial.workspace_name || workspaceName,
  );
  const [role, setRole] = useState(initial.role_title);
  const [workspaceState, setWorkspaceState] = useState(workspace);
  const [plansOpen, setPlansOpen] = useState(false);
  const [activeSection, setActiveSection] = useState<typeof settingsSections[number]["id"]>("account");
  const [collaborationPreferences, setCollaborationPreferences] = useState<
    Record<string, boolean>
  >({
    Mentions: initial.mentions_notifications,
    Replies: initial.reply_notifications,
    "Shared with me": initial.shared_notifications,
  });

  const normalizedQuery = query.trim().toLowerCase();
  const visibleSections = useMemo(
    () => new Set(
      settingsSections
        .filter((section) => !normalizedQuery || section.label.toLowerCase().includes(normalizedQuery))
        .map((section) => section.id),
    ),
    [normalizedQuery],
  );

  const save = (next: WorkspacePreferences) => {
    const revision = ++saveRevisionRef.current;
    setPreferences(next);
    setSaved(false);
    setSaveError(null);
    saveQueueRef.current = saveQueueRef.current
      .catch(() => undefined)
      .then(async () => {
        const response = await fetch("/api/workspace/preferences", {
          method: "PUT",
          headers: { "content-type": "application/json" },
          body: JSON.stringify(next),
          keepalive: true,
        });
        const payload = await response.json().catch(() => null);
        if (!response.ok) {
          throw new Error(payload?.message ?? "Settings could not be saved.");
        }
        if (revision !== saveRevisionRef.current) return;
        const persisted = payload as WorkspacePreferences;
        setPreferences(persisted);
        setSaved(true);
      })
      .catch((error) => {
        if (revision !== saveRevisionRef.current) return;
        setSaveError(
          error instanceof Error ? error.message : "Settings could not be saved.",
        );
      });
    return saveQueueRef.current;
  };

  useEffect(() => {
    const root = document.documentElement;
    const media = window.matchMedia("(prefers-color-scheme: light)");
    const applyTheme = () => {
      root.dataset.theme = preferences.theme === "system"
        ? (media.matches ? "light" : "dark")
        : preferences.theme;
      root.dataset.themePreference = preferences.theme;
    };
    applyTheme();
    localStorage.setItem("oslo-theme", preferences.theme);
    media.addEventListener("change", applyTheme);
    return () => media.removeEventListener("change", applyTheme);
  }, [preferences.theme]);

  useEffect(() => {
    const syncSectionFromHash = () => {
      const section = window.location.hash.slice(1);
      if (settingsSections.some(({ id }) => id === section)) {
        setActiveSection(section as typeof settingsSections[number]["id"]);
      }
    };
    syncSectionFromHash();
    window.addEventListener("hashchange", syncSectionFromHash);
    return () => window.removeEventListener("hashchange", syncSectionFromHash);
  }, []);

  const toggleCollaborationNotification = (title: string) => {
    setCollaborationPreferences((current) => {
      const next = { ...current, [title]: !current[title] };
      void save({
        ...preferences,
        mentions_notifications: next.Mentions,
        reply_notifications: next.Replies,
        shared_notifications: next["Shared with me"],
      });
      return next;
    });
  };

  const commitLocalIdentity = () => {
    void save({
      ...preferences,
      display_name: localDisplayName.trim() || displayName,
      role_title: role.trim(),
      workspace_name: localWorkspaceName.trim() || workspaceName,
    });
  };

  const sectionVisible = (id: typeof settingsSections[number]["id"]) => visibleSections.has(id);
  const memberCount = workspaceState?.member_count ?? 1;
  const collaboratorSeatsUsed = workspaceState?.collaborator_seats_used ?? memberCount;
  const activeProjects = workspaceState?.projects.filter((project) => !project.archived).length ?? 1;
  const activeProjectLimit = workspaceState?.plan === "basic" ? 3 : 1;
  const nextMonth = new Date();
  nextMonth.setMonth(nextMonth.getMonth() + 1, 1);
  const analysisReset = nextMonth.toLocaleDateString("en-GB", { day: "numeric", month: "long" });

  return (
    <main className="settings-shell">
      <aside className="settings-sidebar">
        <Link className="settings-back" href="/workspace"><ArrowLeft size={15} /> Workspace</Link>
        <nav aria-label="Settings">
          {["You", "Workspace", "Plan"].map((group) => (
            <div className="settings-nav-group" key={group}>
              <p>{group}</p>
              {settingsSections.filter((section) => section.group === group).map(({ id, label, ...section }) => (
                <a
                  aria-current={activeSection === id ? "page" : undefined}
                  className={activeSection === id ? "is-active" : undefined}
                  href={`#${id}`}
                  key={id}
                  onClick={() => setActiveSection(id)}
                >
                  <span>{label}</span>
                  {"badge" in section ? <small>{section.badge}</small> : null}
                </a>
              ))}
            </div>
          ))}
        </nav>
      </aside>

      <section className="settings-content">
        <header className="settings-page-heading">
          <div>
            <p>Account & workspace</p>
            <h1>Account & workspace</h1>
            <span>
              Your preferences are separate from project analysis and never change your project evidence.
            </span>
          </div>
          {saved ? <em><Check size={14} /> Saved</em> : null}
        </header>
        {saveError ? <p className="settings-save-error" role="alert">{saveError}</p> : null}

        <label className="settings-search">
          <MagnifyingGlass aria-hidden="true" size={17} />
          <span className="sr-only">Search settings</span>
          <input
            aria-label="Search settings"
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Search settings..."
            type="search"
            value={query}
          />
          {query ? <button aria-label="Clear search" onClick={() => setQuery("")} type="button"><X size={15} /></button> : null}
        </label>

        {sectionVisible("account") ? (
          <article className="settings-section" id="account">
            <div className="settings-section-heading"><h2>Account</h2><p>Your sign-in and session on this device.</p></div>
            <div className="settings-card">
              <div className="settings-row"><span>Email</span><strong>{email ?? `${displayName.toLowerCase().replace(/\s+/g, ".")}@intralign.local`}</strong></div>
              <div className="settings-row"><span>Stay signed in</span><button aria-pressed="true" className="settings-switch is-on" type="button"><i /></button></div>
              <div className="settings-row">
                <span>Your session stays open on this device.</span>
                {logoutAction ? <form action={logoutAction}><button className="settings-secondary-button" type="submit"><SignOut size={15} /> Sign out</button></form> : <button className="settings-secondary-button" type="button"><SignOut size={15} /> Sign out</button>}
              </div>
              <div className="settings-row"><span>Password</span><small>Managed through your invitation and secure sign-in.</small></div>
              <div className="settings-row"><span>Delete account</span><button className="settings-danger-button" onClick={() => setDeleteOpen(true)} type="button"><Trash size={15} /> Delete account</button></div>
            </div>
          </article>
        ) : null}

        {sectionVisible("profile") ? (
          <article className="settings-section" id="profile">
            <div className="settings-section-heading"><h2>Profile</h2><p>Your name as it appears across Intralign.</p></div>
            <div className="settings-card">
              <label className="settings-field-row"><span>Display name</span><input onBlur={commitLocalIdentity} onChange={(event) => setLocalDisplayName(event.target.value)} value={localDisplayName} /></label>
              <label className="settings-field-row"><span>Role or title <small>optional</small></span><input onBlur={commitLocalIdentity} onChange={(event) => setRole(event.target.value)} placeholder="e.g. Programme lead" value={role} /></label>
              <div className="settings-row"><span>Avatar</span><small>Your initials — {localDisplayName.split(/\s+/).map((part) => part[0]).join("").slice(0, 2).toUpperCase()}. Picture upload comes later.</small></div>
            </div>
          </article>
        ) : null}

        {sectionVisible("appearance") ? (
          <article className="settings-section" id="appearance">
            <div className="settings-section-heading"><h2>Appearance</h2><p>Theme and accessibility. Dark is the default.</p></div>
            <div className="settings-card">
              <div className="settings-field-row">
                <span>Theme</span>
                <div className="theme-options">
                  {([
                    ["dark", "Dark", Moon],
                    ["light", "Light", Sun],
                  ] as const).map(([theme, label, Icon]) => (
                    <button
                      aria-label={label}
                      aria-pressed={preferences.theme === theme}
                      className={preferences.theme === theme ? "is-selected" : ""}
                      onClick={() => save({ ...preferences, theme })}
                      type="button"
                      key={theme}
                    >
                      <Icon size={15} /><strong>{label}</strong>
                    </button>
                  ))}
                </div>
              </div>
              <div className="settings-row"><span>Use device theme</span><button className="settings-secondary-button" onClick={() => save({ ...preferences, theme: "system" })} type="button"><Desktop size={15} /> Match system</button></div>
              <div className="settings-row"><span>Reduced motion</span><small>Honoured — follows your operating system</small></div>
              <div className="settings-row"><span>Focus indicators</span><small>Always visible</small></div>
            </div>
          </article>
        ) : null}

        {sectionVisible("notifications") ? (
          <article className="settings-section" id="notifications">
            <div className="settings-section-heading"><h2>Notifications</h2><p>Awareness only — notification choices never start analysis.</p></div>
            <div className="settings-card">
              {collaborationNotifications.map(([title, detail]) => (
                <div className="settings-row" key={title}>
                  <span><strong>{title}</strong><small>{detail}</small></span>
                  <div className="settings-future-control">
                    <span>{collaborationPreferences[title] ? "On" : "Off"}</span>
                    <button
                      aria-checked={collaborationPreferences[title]}
                      aria-label={title}
                      className={`settings-switch ${collaborationPreferences[title] ? "is-on" : ""}`}
                      onClick={() => toggleCollaborationNotification(title)}
                      role="switch"
                      type="button"
                    ><i /></button>
                  </div>
                </div>
              ))}
              {([
                ["analysis_notifications", "Analysis complete", "when OSLO finishes reading your project"],
                ["failure_notifications", "Analysis failed", "when a run could not complete — your last-good read is kept"],
                ["stale_notifications", "Analysis behind your edits", "when your plan has moved on since OSLO last read it"],
              ] as const).map(([key, title, detail]) => (
                <div className="settings-row" key={key}>
                  <span><strong>{title}</strong><small>{detail}</small></span>
                  <div className="settings-future-control">
                    <span>{preferences[key] ? "On" : "Off"}</span>
                    <button
                      aria-checked={preferences[key]}
                      aria-label={title}
                      className={`settings-switch ${preferences[key] ? "is-on" : ""}`}
                      onClick={() => save({ ...preferences, [key]: !preferences[key] })}
                      role="switch"
                      type="button"
                    ><i /></button>
                  </div>
                </div>
              ))}
            </div>
          </article>
        ) : null}

        {sectionVisible("workspace") ? (
          <article className="settings-section" id="workspace">
            <div className="settings-section-heading"><h2>Workspace</h2><p>The container your projects live in.</p></div>
            <div className="settings-card">
              <label className="settings-field-row">
                <span>Workspace name</span>
                <input
                  disabled={preferences.actor_role !== "owner"}
                  onBlur={commitLocalIdentity}
                  onChange={(event) => setLocalWorkspaceName(event.target.value)}
                  value={localWorkspaceName}
                />
                {preferences.actor_role !== "owner" ? (
                  <small>Only a workspace owner can rename the workspace.</small>
                ) : null}
              </label>
              <div className="settings-row"><span>Workspace icon</span><small>First letter — {localWorkspaceName.slice(0, 1).toUpperCase()}. Picture upload comes later.</small></div>
            </div>
          </article>
        ) : null}

        {sectionVisible("project-defaults") ? (
          <article className="settings-section" id="project-defaults">
            <div className="settings-section-heading"><h2>Project defaults</h2><p>Applied to new projects. Never used to gate or block anything.</p></div>
            <div className="settings-card"><div className="settings-row"><span>Default project type</span><small>None — OSLO reads the project you give it</small></div><div className="settings-row"><span>Default workflow</span><small>Classical project management</small></div></div>
          </article>
        ) : null}

        {sectionVisible("collaboration") ? (
          <article className="settings-section" id="collaboration">
            <div className="settings-section-heading"><h2>Collaboration</h2><p>Governed access, review links, comments, and retained snapshots.</p></div>
            <div className="settings-card">
              <div className="settings-row"><span><strong>Default sharing</strong><small>New projects remain private until you share them.</small></span><strong>Private</strong></div>
              <div className="settings-row">
                <span><strong>Owner seats</strong><small>Every workspace member is an Owner. External reviewers do not become members or consume a seat.</small></span>
                <strong>{workspaceState ? `${workspaceState.collaborator_seat_limit} on ${workspaceState.plan_label}` : "3 on Free"}</strong>
              </div>
              <div className="settings-row"><span><strong>External reviewers</strong><small>Review links do not create membership or use a seat.</small></span><strong>Unlimited</strong></div>
              <div className="settings-row"><span><strong>Snapshot links</strong><small>Read-only, revocable, and retained for 30 days.</small></span><strong>30 days</strong></div>
              <div className="settings-row"><span><strong>Review links</strong><small>One attested response; expires after 14 days or issue resolution.</small></span><strong>14 days</strong></div>
              <div className="settings-row">
                <span>Workspace invitations</span>
                {(workspaceState?.role ?? preferences.actor_role) === "owner" ? (
                  <Link href="/admin/invitations">Manage invitations</Link>
                ) : (
                  <small>Managed by workspace owners</small>
                )}
              </div>
            </div>
          </article>
        ) : null}

        {sectionVisible("access") ? (
          <article className="settings-section" id="access">
            <div className="settings-section-heading"><h2>Access &amp; invites</h2><p>How many new people you can bring into OSLO.</p></div>
            <div className="settings-card">
              <div className="settings-row"><span>Release phase</span><span className="settings-fact-pill">GA</span></div>
              <div className="settings-row settings-row-start">
                <span>Invite allocation<small>Spent on a <strong>new</strong> person only.</small></span>
                <span className="settings-row-value"><strong>Retired at GA</strong><small>Limits are now tier-based</small></span>
              </div>
              <div className="settings-row"><span>Waitlist</span><span className="settings-fact-pill">Retired at GA</span></div>
              <div className="settings-row">
                <span>Invite people</span>
                {(workspaceState?.role ?? preferences.actor_role) === "owner" ? (
                  <Link className="settings-primary-link" href="/admin/invitations">Manage invitations →</Link>
                ) : (
                  <small>Managed by workspace owners</small>
                )}
              </div>
            </div>
            <p className="settings-section-note"><strong>Asking anyone for their read is free — no invite, no seat.</strong></p>
            <p className="settings-section-note">GA is active: the allocation and waitlist are retired. Invitations now follow your plan’s seat capacity.</p>
          </article>
        ) : null}

        {sectionVisible("membership") ? (
          <article className="settings-section" id="membership">
            <div className="settings-section-heading"><h2>Membership <small>View</small></h2><p>Who is in this workspace. Nothing here grants or removes access.</p></div>
            <div className="settings-card">
              <div className="settings-row">
                <span><strong>{localDisplayName}</strong><small>{email ?? "Workspace member"}</small></span>
                <strong>{(workspaceState?.role ?? preferences.actor_role).replace(/^\w/, (letter) => letter.toUpperCase())}</strong>
              </div>
              <div className="settings-row">
                <span>
                  {`${memberCount} ${memberCount === 1 ? "member" : "members"}`}
                </span>
                {(workspaceState?.role ?? preferences.actor_role) === "owner" ? (
                  <Link href="#collaboration" onClick={() => setActiveSection("collaboration")}>Manage in Collaboration →</Link>
                ) : (
                  <small>Owner-managed</small>
                )}
              </div>
              <div className="settings-row settings-row-start">
                <span>Owner seats<small>Every workspace member has the same Owner access.</small></span>
                <strong>{`${collaboratorSeatsUsed} of ${workspaceState?.collaborator_seat_limit ?? 3} filled`}</strong>
              </div>
            </div>
          </article>
        ) : null}

        {sectionVisible("subscription") ? (
          <article className="settings-section" id="subscription">
            <div className="settings-section-heading"><h2>Subscription <small>View</small></h2><p>Your plan, what you’re using, and what Basic adds.</p></div>
            <div className="settings-card">
              <div className="settings-row"><span>Plan</span><strong>{workspaceState?.plan_label ?? "Free"}</strong></div>
              <div className="settings-row settings-row-start"><span>Active projects<small>Free <strong>1</strong> · Basic <strong>3</strong>.</small></span><strong>{activeProjects <= activeProjectLimit ? `${activeProjects} of ${activeProjectLimit} active ${activeProjects === 1 ? "project" : "projects"}` : `${activeProjects} active projects · ${activeProjectLimit} included`}</strong></div>
              {activeProjects > activeProjectLimit ? <div className="settings-cap-note">Existing projects remain available. The limit only gates adding another project.</div> : null}
              <div className="settings-row settings-row-start"><span>Owner seats<small>Free <strong>3</strong> (including you) · Basic <strong>10</strong>.</small></span><strong>{`${collaboratorSeatsUsed} of ${workspaceState?.collaborator_seat_limit ?? 3} filled`}</strong></div>
              <div className="settings-row settings-row-start"><span>If you downgrade over the seat limit<small>The limit gates who you can <strong>add</strong>.</small></span><span className="settings-fact-pill">No one is ever removed</span></div>
              <div className="settings-row settings-row-start"><span>Monthly analyses<small>The one limit OSLO surfaces.</small></span><span className="settings-row-value"><strong>{workspaceState?.monthly_analysis_limit == null ? "Not yet set" : `${workspaceState?.monthly_analyses_used ?? 0} analyses used this month`}</strong><small>{workspaceState?.monthly_analysis_limit == null ? "Nothing is enforced" : `resets ${analysisReset}`}</small></span></div>
              <div className="settings-row settings-row-start"><span>Beyond the monthly budget<small>Paid plans: metered overage, against a spend cap you set.</small></span><span className="settings-fact-pill">No silent overspend</span></div>
              <div className="settings-row settings-row-start"><span>Invite allocation<small>Separate from your plan.</small></span><strong>Retired at GA</strong></div>
              <div className="settings-row"><span>Export formats</span><strong>{workspaceState?.plan === "basic" ? "PDF · Copy summary · Export link" : "PDF"}</strong></div>
              <div className="settings-row settings-row-start"><span>Documents<small><strong>Never metered.</strong></small></span><span className="settings-fact-pill">Unlimited on every plan</span></div>
              <div className="settings-row settings-row-start"><span>History<small><strong>Never expires, never truncated.</strong></small></span><span className="settings-fact-pill">Full History on every plan</span></div>
              <div className="settings-row"><span>Link revocation &amp; purpose-scoped expiry</span><span className="settings-fact-pill">On every plan</span></div>
              <div className="settings-row"><span>Review requests and reviewer grants</span><span className="settings-fact-pill">Unlimited on every plan</span></div>
              <div className="settings-row"><span>Compare the plans</span><button className="settings-primary-button" onClick={() => setPlansOpen(true)} type="button">Free vs Basic</button></div>
            </div>
            <p className="settings-section-note"><strong>Free gives you the whole read.</strong> Basic adds capacity and scope.</p>
            <p className="settings-section-note"><strong>What is metered:</strong> analysis runs, project and seat capacity, and labour OSLO does for you.</p>
          </article>
        ) : null}

        {sectionVisible("billing") ? (
          <article className="settings-section" id="billing">
            <div className="settings-section-heading"><h2>Billing <small>Stub</small></h2><p>Not built in this release.</p></div>
            <div className="settings-card"><div className="settings-row"><span>Payment method</span><small>Not built in this release</small></div><div className="settings-row"><span>Invoices</span><small>Not built in this release</small></div><div className="settings-row"><span>Price of Basic</span><strong>$12 / month</strong></div><div className="settings-row"><span>The forward ladder</span><small>Pro ~$39/mo · Team ~$99–149/seat · Enterprise custom</small></div></div>
            <p className="settings-section-note">Upgrading is preview-only. No card is stored and no charge is made.</p>
          </article>
        ) : null}

        {sectionVisible("integrations") ? (
          <article className="settings-section" id="integrations">
            <div className="settings-section-heading"><h2>Integrations <small>Later</small></h2><p>Connecting other tools. Not built yet.</p></div>
            <div className="settings-card">
              <div className="settings-row"><span>Connected tools</span><small>None</small></div>
              <div className="settings-row"><span>Connecting a tool</span><span className="settings-later-pill"><Gear size={13} /> Arrives after this release</span></div>
            </div>
            <p className="settings-section-note">Bring documents to OSLO today. Direct connections come later.</p>
          </article>
        ) : null}

        {!visibleSections.size ? <div className="settings-empty"><MagnifyingGlass size={23} /><strong>No settings found</strong><button onClick={() => setQuery("")} type="button">Clear search</button></div> : null}
      </section>

      {workspaceState ? (
        <PlanComparisonModal
          onClose={() => setPlansOpen(false)}
          onWorkspaceChange={setWorkspaceState}
          open={plansOpen}
          workspace={workspaceState}
        />
      ) : null}

      {deleteOpen ? (
        <div className="workspace-modal-backdrop">
          <section aria-labelledby="delete-account-title" aria-modal="true" role="dialog">
            <span className="workspace-modal-icon is-danger"><Trash size={20} /></span>
            <h2 id="delete-account-title">Delete account?</h2>
            <p>Account deletion is not enabled in Alpha. Contact your workspace owner if you need access removed.</p>
            <div className="workspace-modal-actions"><button onClick={() => setDeleteOpen(false)} type="button">Keep account</button></div>
          </section>
        </div>
      ) : null}
    </main>
  );
}
