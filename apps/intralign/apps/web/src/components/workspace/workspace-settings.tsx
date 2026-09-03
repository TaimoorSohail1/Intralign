"use client";

import {
  Check,
  Desktop,
  Gear,
  Moon,
  Sun,
  UserPlus,
  X,
} from "@phosphor-icons/react";
import { useEffect, useMemo, useRef, useState } from "react";

import { PlanComparisonModal } from "@/components/workspace/plan-comparison-modal";
import type { InvitationSummary, WorkspacePreferences, WorkspaceSummary } from "@/lib/server/oslo-api";

const settingsSections = [
  { id: "profile", label: "Profile", group: "You" },
  { id: "appearance", label: "Appearance", group: "You" },
  { id: "notifications", label: "Notifications", group: "You" },
  { id: "workspace", label: "Workspace", group: "Workspace" },
  { id: "collaboration", label: "Collaboration", group: "Workspace" },
  { id: "access", label: "Access & invites", group: "Workspace" },
  { id: "membership", label: "Membership", group: "Workspace", badge: "View" },
  { id: "plan", label: "Plan & usage", group: "Plan" },
  { id: "billing", label: "Billing", group: "Plan" },
  { id: "integrations", label: "Integrations", group: "Plan", badge: "Later" },
] as const;

export type SettingsSectionId = (typeof settingsSections)[number]["id"];

const roleOptions = [
  ["I run the plan", "Delivery / project PM"],
  ["I own the outcome", "Business / functional owner"],
  ["I own it and run it", "Outcome owner + delivery lead"],
  ["Something else", "Other / not sure"],
] as const;

const collaborationNotifications = [
  ["Mentions", "when someone mentions you"],
  ["Replies", "when someone replies to you"],
  ["Shared with me", "when a project is shared with you"],
] as const;

const transientSettingsStatuses = new Set([408, 425, 429]);

function waitForSettingsRetry(signal: AbortSignal) {
  return new Promise<void>((resolve, reject) => {
    const timer = window.setTimeout(() => {
      signal.removeEventListener("abort", abort);
      resolve();
    }, 160);
    const abort = () => {
      window.clearTimeout(timer);
      reject(new DOMException("The settings request was aborted.", "AbortError"));
    };
    signal.addEventListener("abort", abort, { once: true });
  });
}

async function loadSettingsResource<T>(url: string, signal: AbortSignal): Promise<T> {
  for (let attempt = 0; attempt < 2; attempt += 1) {
    let response: Response;
    try {
      response = await fetch(url, { signal });
    } catch (reason) {
      if (signal.aborted || attempt === 1) throw reason;
      await waitForSettingsRetry(signal);
      continue;
    }

    if (response.ok) return response.json() as Promise<T>;

    const payload = await response.json().catch(() => null);
    const transient = response.status >= 500 || transientSettingsStatuses.has(response.status);
    if (transient && attempt === 0) {
      await waitForSettingsRetry(signal);
      continue;
    }
    throw new Error(payload?.message ?? "Settings could not be loaded.");
  }
  throw new Error("Settings could not be loaded.");
}

export function WorkspaceSettingsDialog({
  displayName,
  initialSection = "profile",
  onClose,
  open,
}: {
  displayName: string;
  initialSection?: SettingsSectionId;
  onClose: () => void;
  open: boolean;
}) {
  const [preferences, setPreferences] = useState<WorkspacePreferences | null>(null);
  const [workspace, setWorkspace] = useState<WorkspaceSummary | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [retry, setRetry] = useState(0);

  useEffect(() => {
    if (!open) return;
    const controller = new AbortController();
    const loadTimer = window.setTimeout(() => {
      setError(null);
      void Promise.all([
        loadSettingsResource<WorkspacePreferences>("/api/workspace/preferences", controller.signal),
        loadSettingsResource<WorkspaceSummary>("/api/workspace", controller.signal),
      ])
        .then(([nextPreferences, nextWorkspace]) => {
          if (controller.signal.aborted) return;
          setPreferences(nextPreferences);
          setWorkspace(nextWorkspace);
        })
        .catch((reason: unknown) => {
          if (controller.signal.aborted) return;
          setError(reason instanceof Error ? reason.message : "Settings could not be loaded.");
        });
    }, 0);
    return () => {
      window.clearTimeout(loadTimer);
      controller.abort();
    };
  }, [open, retry]);

  if (!open) return null;
  if (!preferences || !workspace) {
    return (
      <div className="settings-modal-backdrop" role="presentation">
        <section aria-label="Settings" aria-modal="true" className="settings-dialog settings-dialog-status" role="dialog">
          <button aria-label="Close settings" className="settings-dialog-close" onClick={onClose} type="button"><X size={18} /></button>
          {error ? (
            <><strong>Settings could not be loaded.</strong><p>{error}</p><button className="settings-primary-button" onClick={() => { setError(null); setRetry((value) => value + 1); }} type="button">Try again</button></>
          ) : <p role="status">Loading settings…</p>}
        </section>
      </div>
    );
  }

  return (
    <WorkspaceSettings
      displayName={displayName}
      initial={preferences}
      initialSection={initialSection}
      modal
      onClose={onClose}
      workspace={workspace}
      workspaceName={workspace.name}
    />
  );
}

export function WorkspaceSettings({
  initial,
  workspaceName,
  displayName,
  email,
  workspace,
  modal = false,
  onClose,
  initialSection = "profile",
}: {
  initial: WorkspacePreferences;
  workspaceName: string;
  displayName: string;
  email?: string;
  logoutAction?: () => Promise<void>;
  workspace?: WorkspaceSummary;
  modal?: boolean;
  onClose?: () => void;
  initialSection?: SettingsSectionId;
}) {
  const initialActorRole = workspace?.role ?? initial.actor_role;
  const safeInitialSection = initialActorRole === "owner"
    || settingsSections.find((section) => section.id === initialSection)?.group === "You"
    ? initialSection
    : "profile";
  const [preferences, setPreferences] = useState(initial);
  const [saved, setSaved] = useState(false);
  const [saveError, setSaveError] = useState<string | null>(null);
  const saveQueueRef = useRef<Promise<void>>(Promise.resolve());
  const saveRevisionRef = useRef(0);
  const [localDisplayName, setLocalDisplayName] = useState(initial.display_name || displayName);
  const [localWorkspaceName, setLocalWorkspaceName] = useState(initial.workspace_name || workspaceName);
  const [role, setRole] = useState(initial.role_title || roleOptions[0][0]);
  const [workspaceState, setWorkspaceState] = useState(workspace);
  const [plansOpen, setPlansOpen] = useState(false);
  const planTransitionRef = useRef(false);
  const [activeSection, setActiveSection] = useState<SettingsSectionId>(safeInitialSection);
  const [invitationManagerOpen, setInvitationManagerOpen] = useState(false);
  const [invitations, setInvitations] = useState<InvitationSummary[]>([]);
  const [invitationEmail, setInvitationEmail] = useState("");
  const [invitationBusy, setInvitationBusy] = useState("");
  const [invitationError, setInvitationError] = useState("");
  const [invitationNotice, setInvitationNotice] = useState("");
  const closeButtonRef = useRef<HTMLButtonElement | null>(null);
  const dialogRef = useRef<HTMLElement | null>(null);
  const [collaborationPreferences, setCollaborationPreferences] = useState<Record<string, boolean>>({
    Mentions: initial.mentions_notifications,
    Replies: initial.reply_notifications,
    "Shared with me": initial.shared_notifications,
  });

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
        if (!response.ok) throw new Error(payload?.message ?? "Settings could not be saved.");
        if (revision !== saveRevisionRef.current) return;
        setPreferences(payload as WorkspacePreferences);
        setSaved(true);
      })
      .catch((reason: unknown) => {
        if (revision !== saveRevisionRef.current) return;
        setSaveError(reason instanceof Error ? reason.message : "Settings could not be saved.");
      });
    return saveQueueRef.current;
  };

  useEffect(() => {
    const storedTheme = localStorage.getItem("oslo-theme");
    if ((storedTheme === "dark" || storedTheme === "light" || storedTheme === "system") && storedTheme !== preferences.theme) {
      const timer = window.setTimeout(() => setPreferences((current) => ({ ...current, theme: storedTheme })), 0);
      return () => window.clearTimeout(timer);
    }
    const root = document.documentElement;
    const media = window.matchMedia("(prefers-color-scheme: light)");
    const applyTheme = () => {
      root.dataset.theme = preferences.theme === "system" ? (media.matches ? "light" : "dark") : preferences.theme;
      root.dataset.themePreference = preferences.theme;
    };
    applyTheme();
    localStorage.setItem("oslo-theme", preferences.theme);
    media.addEventListener("change", applyTheme);
    return () => media.removeEventListener("change", applyTheme);
  }, [preferences.theme]);

  useEffect(() => {
    if (!modal) return;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    dialogRef.current?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") onClose?.();
      if (event.key !== "Tab" || !dialogRef.current) return;
      const controls = Array.from(dialogRef.current.querySelectorAll<HTMLElement>('button:not([disabled]), a[href], input:not([disabled]), [tabindex]:not([tabindex="-1"])'));
      if (!controls.length) return;
      const first = controls[0];
      const last = controls[controls.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => {
      document.body.style.overflow = previousOverflow;
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [modal, onClose]);

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

  const commitIdentity = (overrides: Partial<WorkspacePreferences> = {}) => void save({
    ...preferences,
    display_name: localDisplayName.trim() || displayName,
    role_title: role.trim(),
    workspace_name: localWorkspaceName.trim() || workspaceName,
    ...overrides,
  });

  const selectTheme = (theme: WorkspacePreferences["theme"]) => {
    localStorage.setItem("oslo-theme", theme);
    void save({ ...preferences, theme });
  };

  const openPlans = () => {
    if (planTransitionRef.current) return;
    setPlansOpen(true);
  };

  const closePlans = () => {
    planTransitionRef.current = true;
    setPlansOpen(false);
    window.setTimeout(() => {
      planTransitionRef.current = false;
    }, 250);
  };

  const loadInvitations = async () => {
    setInvitationBusy("load");
    setInvitationError("");
    try {
      const response = await fetch("/api/workspace/invitations");
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(payload?.message ?? "Invitations could not be loaded.");
      setInvitations(Array.isArray(payload) ? payload : []);
    } catch (reason) {
      setInvitationError(reason instanceof Error ? reason.message : "Invitations could not be loaded.");
    } finally {
      setInvitationBusy("");
    }
  };

  const showInvitationManager = () => {
    setActiveSection("access");
    setInvitationManagerOpen(true);
    setInvitationNotice("");
    void loadInvitations();
  };

  const sendWorkspaceInvitation = async () => {
    const emailAddress = invitationEmail.trim().toLowerCase();
    if (!emailAddress) return;
    setInvitationBusy("invite");
    setInvitationError("");
    setInvitationNotice("");
    try {
      const response = await fetch("/api/workspace/invitations", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ action: "invite", email: emailAddress }),
      });
      const payload = await response.json().catch(() => null);
      if (!response.ok) throw new Error(payload?.message ?? "The invitation could not be sent.");
      setInvitationEmail("");
      setInvitationNotice(`Invitation sent to ${emailAddress}.`);
      await loadInvitations();
    } catch (reason) {
      setInvitationError(reason instanceof Error ? reason.message : "The invitation could not be sent.");
      setInvitationBusy("");
    }
  };

  const revokeWorkspaceInvitation = async (invitation: InvitationSummary) => {
    setInvitationBusy(invitation.id);
    setInvitationError("");
    setInvitationNotice("");
    try {
      const response = await fetch("/api/workspace/invitations", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ action: "revoke", invitationId: invitation.id }),
      });
      if (!response.ok) {
        const payload = await response.json().catch(() => null);
        throw new Error(payload?.message ?? "The invitation could not be revoked.");
      }
      setInvitations((current) => current.filter((item) => item.id !== invitation.id));
      setInvitationNotice(`Invitation revoked for ${invitation.email}.`);
    } catch (reason) {
      setInvitationError(reason instanceof Error ? reason.message : "The invitation could not be revoked.");
    } finally {
      setInvitationBusy("");
    }
  };

  const memberCount = workspaceState?.member_count ?? 1;
  const collaboratorSeatsUsed = workspaceState?.collaborator_seats_used ?? memberCount;
  const activeProjects = workspaceState?.projects.filter((project) => !project.archived).length ?? 1;
  const activeProjectLimit = workspaceState?.active_project_limit ?? (workspaceState?.plan === "basic" ? 3 : 1);
  const isBasicPlan = workspaceState?.plan === "basic";
  const actorRole = workspaceState?.role ?? preferences.actor_role;
  const visibleSettingsSections = useMemo(
    () => actorRole === "owner"
      ? settingsSections
      : settingsSections.filter((section) => section.group === "You"),
    [actorRole],
  );

  const content = (
    <section className={`settings-dialog is-${activeSection}`} ref={dialogRef} role={modal ? "dialog" : undefined} aria-modal={modal ? "true" : undefined} aria-labelledby="settings-dialog-title" tabIndex={-1}>
      <header className="settings-dialog-header">
        <div><h1 id="settings-dialog-title">Settings</h1><span>account · notifications · workspace · collaboration · billing</span></div>
        {saved ? <em role="status"><Check size={14} /> Saved</em> : null}
        {modal ? <button aria-label="Close settings" className="settings-dialog-close" onClick={onClose} ref={closeButtonRef} type="button"><X size={18} /></button> : null}
      </header>
      <div className="settings-dialog-body">
        <aside className="settings-sidebar">
          <nav aria-label="Settings">
            {["You", "Workspace", "Plan"].map((group) => (
              visibleSettingsSections.some((section) => section.group === group) ?
              <div className="settings-nav-group" key={group}>
                <p>{group}</p>
                {visibleSettingsSections.filter((section) => section.group === group).map(({ id, label, ...section }) => (
                  <button aria-current={activeSection === id ? "page" : undefined} className={activeSection === id ? "is-active" : undefined} key={id} onClick={() => setActiveSection(id)} type="button">
                    <span>{label}</span>{"badge" in section ? <small>{section.badge}</small> : null}
                  </button>
                ))}
              </div> : null
            ))}
          </nav>
        </aside>

        <div className="settings-content">
          {saveError ? <p className="settings-save-error" role="alert">{saveError}</p> : null}

          {activeSection === "profile" ? <article className="settings-section" id="profile">
            <div className="settings-section-heading"><h2>Profile</h2><p>Your name as it shows across OSLO.</p></div>
            <div className="settings-card">
              <label className="settings-field-row"><span>Display name</span><input aria-label="Display name" onBlur={() => commitIdentity()} onChange={(event) => setLocalDisplayName(event.target.value)} value={localDisplayName} /></label>
              <div className="settings-row"><span>Email</span><strong>{email ?? `${displayName.toLowerCase().replace(/\s+/g, ".")}@intralign.local`}</strong></div>
              <div className="settings-choice-block"><strong>How you work</strong><p>Changes only which first move OSLO puts first — never your read, band, or issues.</p><div className="settings-role-options">{roleOptions.map(([title, detail]) => <button aria-pressed={role === title} className={role === title ? "is-selected" : ""} key={title} onClick={() => { setRole(title); commitIdentity({ role_title: title }); }} type="button"><strong>{title}</strong><small>{detail}</small></button>)}</div></div>
            </div>
          </article> : null}

          {activeSection === "appearance" ? <article className="settings-section" id="appearance">
            <div className="settings-section-heading"><h2>Appearance</h2><p>Theme and accessibility. Dark is the default.</p></div>
            <div className="settings-card">
              <div className="settings-field-row"><span>Theme</span><div className="theme-options">{([["dark", "Dark", Moon], ["light", "Light", Sun]] as const).map(([theme, label, Icon]) => <button aria-label={label} aria-pressed={preferences.theme === theme} className={preferences.theme === theme ? "is-selected" : ""} key={theme} onClick={() => selectTheme(theme)} type="button"><Icon size={15} /><strong>{label}</strong></button>)}</div></div>
              <div className="settings-row"><span>Use device theme</span><button className="settings-secondary-button" onClick={() => selectTheme("system")} type="button"><Desktop size={15} /> Match system</button></div>
              <div className="settings-row"><span>Reduced motion</span><small>Honoured — follows your operating system</small></div>
              <div className="settings-row"><span>Focus indicators</span><small>Always visible</small></div>
            </div>
          </article> : null}

          {activeSection === "notifications" ? <article className="settings-section" id="notifications">
            <div className="settings-section-heading"><h2>Notifications</h2><p>Awareness only — notification choices never start analysis.</p></div>
            <div className="settings-card">
              {collaborationNotifications.map(([title, detail]) => <SettingsSwitch detail={detail} key={title} label={title} onClick={() => toggleCollaborationNotification(title)} value={collaborationPreferences[title]} />)}
              {([[
                "analysis_notifications", "Analysis complete", "when OSLO finishes reading your project",
              ], ["failure_notifications", "Analysis failed", "when a run could not complete — your last-good read is kept"], ["stale_notifications", "Analysis behind your edits", "when your plan has moved on since OSLO last read it"]] as const).map(([key, title, detail]) => <SettingsSwitch detail={detail} key={key} label={title} onClick={() => void save({ ...preferences, [key]: !preferences[key] })} value={preferences[key]} />)}
            </div>
          </article> : null}

          {activeSection === "workspace" ? <article className="settings-section" id="workspace">
            <div className="settings-section-heading"><h2>Workspace</h2><p>The container your projects live in.</p></div>
            <div className="settings-card">
              <label className="settings-field-row"><span>Workspace name</span><input aria-label="Workspace name" disabled={preferences.actor_role !== "owner"} onBlur={() => commitIdentity()} onChange={(event) => setLocalWorkspaceName(event.target.value)} value={localWorkspaceName} /></label>
              <div className="settings-row"><span>Workspace icon</span><small>First letter — {localWorkspaceName.slice(0, 1).toUpperCase()}. Picture upload comes later.</small></div>
              <div className="settings-row"><span>New-project defaults</span><small>None — OSLO reads the project you give it.</small></div>
            </div>
          </article> : null}

          {activeSection === "collaboration" ? <article className="settings-section" id="collaboration">
            <div className="settings-section-heading"><h2>Collaboration</h2><p>Governed access, review links, comments, and retained snapshots.</p></div>
            <div className="settings-card">
              <Fact label="Default sharing" detail="New projects remain private until you share them." value="Private" />
              <Fact label="Workspace members" detail="Members, reviewers and viewers never consume plan capacity." value="Not capacity-gated" />
              <Fact label="External reviewers" detail="Review links do not create membership or use a seat." value="Unlimited" />
              <Fact label="Snapshot links" detail="Read-only, revocable, and retained for 30 days." value="30 days" />
              <Fact label="Review links" detail="One attested response; expires after 14 days or issue resolution." value="14 days" />
              {actorRole === "owner" ? <div className="settings-row"><span><strong>Workspace access</strong><small>Invite people and revoke pending invitations without leaving Settings.</small></span><button className="settings-link-button" onClick={showInvitationManager} type="button">Manage invitations →</button></div> : null}
            </div>
          </article> : null}

          {activeSection === "access" ? <article className="settings-section" id="access">
            <div className="settings-section-heading"><h2>Access &amp; invites</h2><p>How new people enter this workspace.</p></div>
            <div className="settings-card"><Fact label="Release phase" value="GA" /><Fact label="Invite allocation" detail="Spent on a new person only." value="Not capacity-gated" /><Fact label="Waitlist" value="Retired at GA" /><div className="settings-row"><span>Invite people</span>{actorRole === "owner" ? <button className="settings-primary-button" onClick={showInvitationManager} type="button">Manage invitations →</button> : <small>Managed by workspace owners</small>}</div></div>
            <p className="settings-section-note"><strong>Asking anyone for their read is free — no invite, no seat.</strong></p>
            {invitationManagerOpen ? <InvitationManager busy={invitationBusy} email={invitationEmail} error={invitationError} invitations={invitations} notice={invitationNotice} onClose={() => setInvitationManagerOpen(false)} onEmailChange={setInvitationEmail} onReload={() => void loadInvitations()} onRevoke={(invitation) => void revokeWorkspaceInvitation(invitation)} onSend={() => void sendWorkspaceInvitation()} /> : null}
          </article> : null}

          {activeSection === "membership" ? <article className="settings-section" id="membership">
            <div className="settings-section-heading"><h2>Membership <small>View</small></h2><p>Who is in this workspace. Nothing here grants or removes access.</p></div>
            <div className="settings-card"><div className="settings-row"><span><strong>{localDisplayName}</strong><small>{email ?? "Workspace member"}</small></span><strong>{actorRole.replace(/^\w/, (letter) => letter.toUpperCase())}</strong></div><div className="settings-row"><span>{memberCount} {memberCount === 1 ? "member" : "members"}</span>{actorRole === "owner" ? <button className="settings-link-button" onClick={showInvitationManager} type="button">Manage access &amp; invitations →</button> : <small>Owner-managed</small>}</div><Fact label="Workspace members" detail="People never consume plan capacity." value={`${collaboratorSeatsUsed} active`} /></div>
          </article> : null}

          {activeSection === "plan" ? <article className="settings-section settings-plan-section" id="plan">
            <div className="settings-section-heading">
              <h2>Plan &amp; usage</h2>
              <p>Where you stand today — your plan, what you’re using, and what more would add. The unit of value is the <strong>outcome</strong>; OSLO never meters the quality of your read.</p>
            </div>
            <div className="settings-plan-current">
              <span>{workspaceState?.plan_label ?? "Free"}</span>
              <strong>You&apos;re on the {workspaceState?.plan_label ?? "Free"} plan — the full-quality read on one outcome, your whole record kept and unmetered.</strong>
            </div>

            <h3>What you&apos;re using</h3>
            <div className="settings-card settings-plan-usage">
              <PlanUsageFact detail={isBasicPlan ? "Basic optimizes every declared outcome." : "The Free plan optimizes your primary outcome. Declaring more is free — the rest are recorded but don’t drive the read until optimized."} label="Outcomes" value="1 optimized · 1 declared" />
              <PlanUsageFact detail={isBasicPlan ? `Basic keeps up to ${activeProjectLimit} plans active at once.` : "The Free plan works one plan at a time — switch whenever; the others are kept, never deleted."} label="Plans" value={`${activeProjects} in your workspace · ${Math.min(activeProjects, activeProjectLimit)} active`} />
              <PlanUsageFact detail="Never metered — attach as much as your plan needs." label="Documents" value="Unlimited" />
              <PlanUsageFact detail="A fair-use ceiling, not a product limit. The unit that matters is the outcome, not analysis count." label="Analyses" value="Generous — fair-use" />
              <PlanUsageFact detail="Never expires, never truncated." label="History" value="Full" />
              <PlanUsageFact detail="Sharing and asking for a read never consume a seat." label="Collaboration" value="Viewers &amp; reviewers free" />
            </div>

            <h3>{isBasicPlan ? "What Basic includes" : "What Basic adds"}</h3>
            <div className="settings-card settings-plan-additions">
              <PlanAddition title="Optimize all your outcomes">OSLO steering your plan toward every outcome at once — not just your primary</PlanAddition>
              <PlanAddition title="Run more than one plan">Working several plans in your workspace at the same time</PlanAddition>
              <PlanAddition title="Read a larger corpus">A bigger intake — more and larger files</PlanAddition>
              <PlanAddition title="Send on a schedule">A recurring weekly send that re-reads for currency before it goes</PlanAddition>
              <PlanAddition title="Push your plan to Asana">A one-way push so you can view it there</PlanAddition>
              <div className="settings-plan-compare">
                <span>{isBasicPlan ? "Review your plan" : "Need more capacity?"}</span>
                <button className="settings-primary-button" onClick={openPlans} type="button">{isBasicPlan ? "Review Free vs Basic" : "Compare Free vs Basic"}</button>
              </div>
            </div>
          </article> : null}

          {activeSection === "billing" ? <article className="settings-section" id="billing">
            <div className="settings-section-heading"><h2>Billing</h2><p>Secure checkout, invoices and cancellation are hosted by Stripe.</p></div>
            <div className="settings-card"><Fact label="Price of Basic" value="$29 / month · $290 / year" /><Fact label="Workspace price" value="Flat · never per seat" /><div className="settings-row"><span>Payment method, invoices and cancellation</span><button className="settings-primary-button" onClick={openPlans} type="button">{workspaceState?.plan === "basic" ? "Manage secure billing" : "View Basic"}</button></div></div>
            <p className="settings-section-note">Basic activates only after Stripe sends a verified payment event. Cancellation preserves every record.</p>
          </article> : null}

          {activeSection === "integrations" ? <article className="settings-section" id="integrations">
            <div className="settings-section-heading"><h2>Integrations <small>Later</small></h2><p>Connecting other tools. Not built yet.</p></div>
            <div className="settings-card"><div className="settings-row"><span>Connected tools</span><small>None</small></div><div className="settings-row"><span>Connecting a tool</span><span className="settings-later-pill"><Gear size={13} /> Arrives after this release</span></div></div>
          </article> : null}
        </div>
      </div>
      {workspaceState ? <PlanComparisonModal onClose={closePlans} onWorkspaceChange={setWorkspaceState} open={plansOpen} workspace={workspaceState} /> : null}
    </section>
  );

  if (!modal) return <main className="settings-standalone">{content}</main>;
  return <div className="settings-modal-backdrop" onMouseDown={(event) => { if (!plansOpen && !planTransitionRef.current && event.currentTarget === event.target) onClose?.(); }} role="presentation">{content}</div>;
}

function SettingsSwitch({ detail, label, onClick, value }: { detail: string; label: string; onClick: () => void; value: boolean }) {
  return <div className="settings-row"><span><strong>{label}</strong><small>{detail}</small></span><div className="settings-future-control"><span>{value ? "On" : "Off"}</span><button aria-checked={value} aria-label={label} className={`settings-switch ${value ? "is-on" : ""}`} onClick={onClick} role="switch" type="button"><i /></button></div></div>;
}

function Fact({ detail, label, value }: { detail?: string; label: string; value: string }) {
  return <div className="settings-row settings-row-start"><span><strong>{label}</strong>{detail ? <small>{detail}</small> : null}</span><strong>{value}</strong></div>;
}

function PlanUsageFact({ detail, label, value }: { detail: string; label: string; value: string }) {
  return <div className="settings-plan-row"><span><strong>{label}</strong><small>{detail}</small></span><b>{value}</b></div>;
}

function PlanAddition({ children, title }: { children: string; title: string }) {
  return <div className="settings-plan-addition"><span aria-hidden="true"><Check size={13} /></span><div><strong>{title}</strong><small>{children}</small></div></div>;
}

function InvitationManager({
  busy,
  email,
  error,
  invitations,
  notice,
  onClose,
  onEmailChange,
  onReload,
  onRevoke,
  onSend,
}: {
  busy: string;
  email: string;
  error: string;
  invitations: InvitationSummary[];
  notice: string;
  onClose: () => void;
  onEmailChange: (email: string) => void;
  onReload: () => void;
  onRevoke: (invitation: InvitationSummary) => void;
  onSend: () => void;
}) {
  const pendingInvitations = invitations.filter((invitation) => invitation.status === "pending");

  return (
    <section aria-labelledby="workspace-invitations-title" className="settings-invitation-manager">
      <header>
        <span>
          <UserPlus aria-hidden="true" size={18} />
          <span><h3 id="workspace-invitations-title">Workspace invitations</h3><small>Invite workspace members without leaving this project.</small></span>
        </span>
        <button aria-label="Close invitation manager" className="settings-dialog-close" onClick={onClose} type="button"><X size={16} /></button>
      </header>
      <form onSubmit={(event) => { event.preventDefault(); onSend(); }}>
        <label htmlFor="workspace-invitation-email">Email address</label>
        <div>
          <input aria-label="Invitation email" autoComplete="email" id="workspace-invitation-email" name="email" onChange={(event) => onEmailChange(event.target.value)} placeholder="name@company.com" type="email" value={email} />
          <button className="settings-primary-button" disabled={busy === "invite" || !email.trim()} type="submit">{busy === "invite" ? "Sending\u2026" : "Send invitation"}</button>
        </div>
      </form>
      {error ? <div className="settings-invitation-message is-error" role="alert"><span>{error}</span><button onClick={onReload} type="button">Try again</button></div> : null}
      {notice ? <p className="settings-invitation-message is-success" role="status"><Check size={14} /> {notice}</p> : null}
      <div className="settings-invitation-list" aria-live="polite">
        <div className="settings-invitation-list-heading"><strong>Pending</strong><span>{pendingInvitations.length}</span></div>
        {busy === "load" ? <p role="status">Loading invitations\u2026</p> : pendingInvitations.length ? pendingInvitations.map((invitation) => (
          <article key={invitation.id}>
            <span><strong>{invitation.email}</strong><small>Expires {new Intl.DateTimeFormat(undefined, { dateStyle: "medium" }).format(new Date(invitation.expires_at))}</small></span>
            <button aria-label={`Revoke ${invitation.email}`} disabled={busy === invitation.id} onClick={() => onRevoke(invitation)} type="button">{busy === invitation.id ? "Revoking\u2026" : "Revoke"}</button>
          </article>
        )) : <p>No pending invitations.</p>}
      </div>
    </section>
  );
}
