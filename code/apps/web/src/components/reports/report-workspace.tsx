"use client";

import {
  ArrowCounterClockwise,
  ArrowClockwise,
  CaretDown,
  CaretRight,
  Check,
  Clock,
  DownloadSimple,
  EnvelopeSimple,
  LinkSimple,
  ListBullets,
  LockSimple,
  MagnifyingGlass,
  Plus,
  Sparkle,
  TextB,
  TextItalic,
  TextUnderline,
  X,
} from "@phosphor-icons/react";
import { useEffect, useMemo, useRef, useState } from "react";
import { createPortal } from "react-dom";

import type {
  AsanaHandoffState,
  OverviewSnapshot,
  ProjectHistory,
  ReportContent,
  ReportSchedule,
} from "@/lib/server/oslo-api";

import { GeneratedReportView } from "./generated-report-view";
import { buildPlanExport } from "./report-export-content";
import { currentReadSummary, projectReportProjection } from "./report-projection";

type ReportView =
  | "executive-briefing"
  | "outcome-readiness"
  | "assumptions-evidence"
  | "decision-record";

const reportViews: Array<{
  id: ReportView;
  name: string;
  ownership: "Authored" | "Generated";
}> = [
  { id: "executive-briefing", name: "Executive Briefing", ownership: "Authored" },
  { id: "outcome-readiness", name: "Outcome Readiness", ownership: "Generated" },
  { id: "assumptions-evidence", name: "Assumptions & Evidence", ownership: "Generated" },
  { id: "decision-record", name: "Decision Record", ownership: "Generated" },
];

type ReportSection = {
  id: string;
  title: string;
  body: string[];
};

type ReportDelivery = {
  id: string;
  recipient_email: string;
  recipient_label: string;
  status: "scheduled" | "sending" | "sent" | "failed";
  scheduled_for: string;
  sent_at: string | null;
  error_code: string | null;
  currency_state: "current" | "previous_analysis";
  previous_analysis_confirmed: boolean;
  report_version: number;
  analysis_completed_at: string;
  content?: ReportContent;
};

const reportSectionOrder = [
  "summary",
  "changed",
  "risks",
  "assumptions",
  "action",
  "decisions",
  "appendix",
] as const;

const defaultBriefingIncludes = {
  integrity: true,
  risks: true,
  grounding: true,
  moves: true,
};

function sentence(value: string | null | undefined, fallback: string) {
  const normalized = value?.trim();
  return normalized || fallback;
}

function uniqueText(values: string[]) {
  const unique = new Map<string, string>();
  for (const value of values) {
    const key = value.toLowerCase().replace(/[^\p{L}\p{N}]+/gu, " ").trim();
    if (key && !unique.has(key)) unique.set(key, value);
  }
  return [...unique.values()];
}

const reportDateFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "2-digit",
  month: "short",
  year: "numeric",
  timeZone: "UTC",
});

const reportDateTimeFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "2-digit",
  month: "short",
  year: "numeric",
  hour: "2-digit",
  minute: "2-digit",
  hour12: false,
  timeZone: "UTC",
});

const reportWeekdays = [
  "Monday",
  "Tuesday",
  "Wednesday",
  "Thursday",
  "Friday",
  "Saturday",
  "Sunday",
] as const;

function sourceDocumentCount(snapshot: OverviewSnapshot) {
  if (snapshot.source_document_count) return snapshot.source_document_count;
  return new Set(
    snapshot.artifacts
      .flatMap((artifact) => artifact.evidence_refs)
      .map((reference) => reference.match(/^document:([^:]+)/)?.[1])
      .filter(Boolean),
  ).size;
}

function audienceDecision(recipient: string, questions: string[]) {
  const openQuestion = questions[0] ?? "No decision is currently required.";
  if (recipient === "Team") {
    return `Please confirm the delivery owner and next practical step: ${openQuestion}`;
  }
  if (recipient === "Board") {
    return `Please resolve the highest-impact open decision: ${openQuestion}`;
  }
  return `Please confirm the decision needed to protect the intended outcome: ${openQuestion}`;
}

function buildSections(
  snapshot: OverviewSnapshot,
  history: ProjectHistory | undefined,
  recipient: string,
): ReportSection[] {
  const issues = snapshot.assessment.issues.filter((issue) => issue.status !== "resolved");
  const currentRun = history?.groups.find((group) => group.current);
  const evidenceCount = new Set(
    snapshot.artifacts.flatMap((artifact) => artifact.evidence_refs),
  ).size;
  const questions = uniqueText(
    issues
      .filter((issue) => issue.clarification)
      .map((issue) => issue.clarification as string),
  );
  const documentedRisks = uniqueText(snapshot.artifacts
    .flatMap((artifact) =>
      (artifact.content?.sections ?? [])
        .filter((section) => section.heading.toLowerCase().includes("risk"))
        .flatMap((section) => [
          ...(section.body.trim() ? [section.body.trim()] : []),
          ...section.bullets.map((item) => item.trim()).filter(Boolean),
          ...section.rows.map((row) => row.filter(Boolean).join(" — ")),
        ]),
    )
    .filter(Boolean));

  return [
    {
      id: "summary",
      title: "Summary",
      body: [
        sentence(
          currentReadSummary(
            snapshot.summary,
            issues.length,
            snapshot.project_title,
          ),
          "The supplied project material forms a usable current view of the plan.",
        ),
        issues.length
          ? `${issues.length} open ${issues.length === 1 ? "point needs" : "points need"} attention before the plan can be treated as settled.`
          : "No material open point remains in the current project read.",
      ],
    },
    {
      id: "changed",
      title: "What changed",
      body: currentRun?.changes.length
        ? currentRun.changes.map((change) => change.label)
        : [
            snapshot.state === "provisional"
              ? "This is the first retained project read."
              : "The latest evidence review is now the current retained project view.",
          ],
    },
    {
      id: "risks",
      title: "Key risks",
      body: documentedRisks.length || issues.length
        ? uniqueText([
            ...documentedRisks,
            ...issues.map(
            (issue) =>
              `${issue.title}. ${issue.why} If it stays unresolved, it may weaken delivery of the intended outcome.`,
            ),
          ]).slice(0, 10)
        : ["No open critical or moderate risk is present in the current read."],
    },
    {
      id: "assumptions",
      title: "Assumptions",
      body: (() => {
        const assumptionsByStatement = new Map<string, string>();
        for (const artifact of snapshot.artifacts) {
          for (const assumption of artifact.assumptions ?? []) {
            const key = assumption.statement
              .toLowerCase()
              .replace(/[^\p{L}\p{N}]+/gu, " ")
              .trim();
            if (!assumptionsByStatement.has(key)) {
              assumptionsByStatement.set(
                key,
                `${artifact.title}: ${assumption.statement}${
                  assumption.load_bearing ? " (load-bearing)" : ""
                }`,
              );
            }
          }
        }
        const assumptions = [...assumptionsByStatement.values()].slice(0, 10);
        return assumptions.length
          ? assumptions
          : ["No material assumption is recorded in the current read."];
      })(),
    },
    {
      id: "action",
      title: "Plan of action",
      body: issues.length
        ? uniqueText(
            issues.map((issue) => `Recommended: ${issue.recommendation}`),
          ).slice(0, 5)
        : ["Recommended: keep the retained plan evidence current and record material changes."],
    },
    {
      id: "decisions",
      title: "Decisions needed",
      body: [audienceDecision(recipient, questions)],
    },
    {
      id: "appendix",
      title: "Appendix",
      body: [
        `${sourceDocumentCount(snapshot)} source documents are represented in this read.`,
        `${snapshot.artifacts.length} plan artifacts were constructed from those sources.`,
        `${evidenceCount} distinct source references support the current document.`,
        `Current as of ${reportDateTimeFormatter.format(new Date(snapshot.published_at))} UTC.`,
      ],
    },
  ];
}

function escapeHtml(value: string) {
  return value
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sectionsToHtml(sections: ReportSection[]) {
  return sections
    .map(
      (section) => `
        <section class="report-editable-section" data-section="${section.id}" id="report-${section.id}">
          <h2>${escapeHtml(section.title)}</h2>
          <div class="report-section-body">
            ${section.body.map((paragraph) => `<p>${escapeHtml(paragraph)}</p>`).join("")}
          </div>
        </section>`,
    )
    .join("");
}

function sanitizeReadoutHtml(value: string) {
  if (typeof document === "undefined") return value;
  const template = document.createElement("template");
  template.innerHTML = value;
  template.content
    .querySelectorAll("script, style, iframe, object, embed, form, input, button")
    .forEach((element) => element.remove());
  template.content.querySelectorAll("*").forEach((element) => {
    for (const attribute of Array.from(element.attributes)) {
      const name = attribute.name.toLowerCase();
      const content = attribute.value.trim().toLowerCase();
      if (
        name.startsWith("on") ||
        name === "style" ||
        (name === "href" && content.startsWith("javascript:"))
      ) {
        element.removeAttribute(attribute.name);
      }
    }
  });
  return template.innerHTML;
}

function editorContent(element: HTMLElement | null, fallback: ReportSection[]): ReportContent {
  if (!element) return { sections: fallback };
  const discovered = Array.from(
    element.querySelectorAll<HTMLElement>(".report-editable-section"),
  ).map((section, index) => {
    const body = Array.from(
      section.querySelectorAll<HTMLElement>(".report-section-body > *"),
    )
      .map((item) => (item.innerText || item.textContent || "").trim())
      .filter(Boolean);
    return {
      id: section.dataset.section || fallback[index]?.id || `section-${index + 1}`,
      title:
        section.querySelector("h2")?.textContent?.trim() ||
        fallback[index]?.title ||
        `Section ${index + 1}`,
      body: body.length ? body : ["No content recorded."],
    };
  });
  const byId = new Map(discovered.map((section) => [section.id, section]));
  return {
    sections: fallback.map((section) => byId.get(section.id) ?? section),
  };
}

function contentToHtml(content: ReportContent) {
  return sectionsToHtml(content.sections);
}

export function ReportWorkspace({
  snapshot,
  history,
}: {
  snapshot: OverviewSnapshot;
  history?: ProjectHistory;
}) {
  const defaultRecipient = "Exec sponsor";
  const initialSections = useMemo(
    () => buildSections(snapshot, history, defaultRecipient),
    [history, snapshot],
  );
  const storageKey = `oslo:readout:${snapshot.project_id}:${snapshot.snapshot_id}`;
  const reportWelcomeKey = `oslo:reports-welcome:${snapshot.project_id}`;
  const initialHtml = useMemo(() => sectionsToHtml(initialSections), [initialSections]);
  const projection = useMemo(
    () => projectReportProjection(snapshot, history),
    [history, snapshot],
  );
  const editorRef = useRef<HTMLDivElement>(null);
  const saveTimerRef = useRef<number | null>(null);
  const reportTabRefs = useRef<Array<HTMLButtonElement | null>>([]);
  const exportDialogRef = useRef<HTMLDivElement>(null);
  const [activeReport, setActiveReport] = useState<ReportView>("executive-briefing");
  const [briefingStage, setBriefingStage] = useState<"compose" | "author" | "sent">("compose");
  const [briefingDepth, setBriefingDepth] = useState<"summary" | "full">("full");
  const [includedBriefingSections, setIncludedBriefingSections] = useState(
    defaultBriefingIncludes,
  );
  const [sectionsOpen, setSectionsOpen] = useState(false);
  const [scheduleOpen, setScheduleOpen] = useState(false);
  const [findOpen, setFindOpen] = useState(false);
  const [findValue, setFindValue] = useState("");
  const [findCount, setFindCount] = useState(0);
  const [recipient, setRecipient] = useState(defaultRecipient);
  const [notice, setNotice] = useState<string | null>(null);
  const [sendOpen, setSendOpen] = useState(false);
  const [exportOpen, setExportOpen] = useState(false);
  const [exportFormat, setExportFormat] = useState<"excel" | "csv" | "text" | "pdf">("pdf");
  const [exportDetailsOpen, setExportDetailsOpen] = useState(false);
  const [editingRecipient, setEditingRecipient] = useState(false);
  const [deliveryEmail, setDeliveryEmail] = useState("");
  const [weeklyDay, setWeeklyDay] = useState("1");
  const [weeklyTime, setWeeklyTime] = useState("09:00");
  const [weeklyTimezone, setWeeklyTimezone] = useState(
    Intl.DateTimeFormat().resolvedOptions().timeZone || "UTC",
  );
  const [deliveryPending, setDeliveryPending] = useState(false);
  const [deliveries, setDeliveries] = useState<ReportDelivery[]>([]);
  const [reportSchedules, setReportSchedules] = useState<ReportSchedule[]>([]);
  const [scheduleActionId, setScheduleActionId] = useState<string | null>(null);
  const [asanaState, setAsanaState] = useState<AsanaHandoffState | null>(null);
  const [asanaPending, setAsanaPending] = useState(false);
  const [showReportWelcome, setShowReportWelcome] = useState(true);
  const [previousDocumentHtml, setPreviousDocumentHtml] = useState<string | null>(null);
  const [draftRevision, setDraftRevision] = useState(1);
  const [documentHtml, setDocumentHtml] = useState(initialHtml);
  const [currentSnapshotId, setCurrentSnapshotId] = useState(snapshot.snapshot_id);
  const isPreviousAnalysis = currentSnapshotId !== snapshot.snapshot_id;

  useEffect(() => {
    let active = true;
    const loadSharedDraft = async () => {
      const deviceHtml = sanitizeReadoutHtml(
        window.localStorage.getItem(storageKey) || "",
      );
      if (deviceHtml) {
        setDocumentHtml(deviceHtml);
        setBriefingStage("author");
      }
      try {
        const response = await fetch(`/api/projects/${snapshot.project_id}/report`);
        if (!response.ok) return;
        const result = (await response.json()) as {
          snapshot_id: string;
          content: ReportContent | null;
          deliveries?: ReportDelivery[];
          recipient_class?: "exec-sponsor" | "team" | "board";
          composition_depth?: "summary" | "full";
          included?: typeof includedBriefingSections;
          revision?: number;
        };
        setCurrentSnapshotId(result.snapshot_id);
        if (active) setDeliveries(result.deliveries ?? []);
        if (active && result.recipient_class) {
          setRecipient(
            result.recipient_class === "exec-sponsor"
              ? "Exec sponsor"
              : result.recipient_class === "team"
                ? "Team"
                : "Board",
          );
        }
        if (active && result.composition_depth) setBriefingDepth(result.composition_depth);
        if (active && result.included && Object.keys(result.included).length) {
          setIncludedBriefingSections(result.included);
        }
        if (active && result.revision) setDraftRevision(result.revision);
        if (!active || result.snapshot_id !== snapshot.snapshot_id) return;
        if (result.content) {
          const html = contentToHtml(result.content);
          setDocumentHtml(html);
          setBriefingStage("author");
          window.localStorage.setItem(storageKey, html);
          return;
        }
        const staging = document.createElement("div");
        staging.innerHTML = deviceHtml || initialHtml;
        await fetch(`/api/projects/${snapshot.project_id}/report`, {
          method: "PUT",
          headers: { "content-type": "application/json" },
          keepalive: true,
          body: JSON.stringify({
            snapshot_id: snapshot.snapshot_id,
            content: editorContent(staging, initialSections),
            recipient_class: "exec-sponsor",
            composition_depth: "full",
            included: defaultBriefingIncludes,
            revision: 1,
          }),
        });
      } catch {
        // The sanitized device copy remains available when the shared draft is offline.
      }
    };
    void loadSharedDraft();
    return () => {
      active = false;
    };
  }, [
    initialHtml,
    initialSections,
    snapshot.project_id,
    snapshot.snapshot_id,
    storageKey,
  ]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setShowReportWelcome(window.localStorage.getItem(reportWelcomeKey) !== "dismissed");
    }, 0);
    return () => window.clearTimeout(timer);
  }, [reportWelcomeKey]);

  useEffect(() => {
    let active = true;
    void fetch(`/api/projects/${snapshot.project_id}/report/schedules`, {
      cache: "no-store",
    })
      .then(async (response) => (response.ok ? response.json() : []))
      .then((result) => {
        if (active) {
          setReportSchedules((current) =>
            current.length ? current : Array.isArray(result) ? result : [],
          );
        }
      })
      .catch(() => {
        // Scheduling is optional; create/update actions surface their own errors.
      });
    return () => {
      active = false;
    };
  }, [snapshot.project_id]);

  useEffect(() => {
    let active = true;
    void fetch(`/api/projects/${snapshot.project_id}/report/asana`, {
      cache: "no-store",
    })
      .then(async (response) => (response.ok ? response.json() : null))
      .then((result) => {
        if (active && result && typeof result.configured === "boolean") {
          setAsanaState(result as AsanaHandoffState);
        }
      })
      .catch(() => {
        // Manual downloads remain available if the connector status is offline.
      });
    return () => {
      active = false;
    };
  }, [snapshot.project_id]);

  useEffect(() => {
    if (!exportOpen) return;
    const previouslyFocused = document.activeElement as HTMLElement | null;
    const dialog = exportDialogRef.current;
    dialog?.querySelector<HTMLElement>("button")?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        setExportOpen(false);
        return;
      }
      if (event.key !== "Tab" || !dialog) return;
      const focusable = Array.from(
        dialog.querySelectorAll<HTMLElement>(
          'button:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex="0"]',
        ),
      );
      if (!focusable.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      previouslyFocused?.focus();
    };
  }, [exportOpen]);

  const persistDocument = async () => {
    const html = sanitizeReadoutHtml(editorRef.current?.innerHTML ?? "");
    if (!html) return { sections: initialSections };
    window.localStorage.setItem(storageKey, html);
    const content = editorContent(editorRef.current, initialSections);
    const response = await fetch(`/api/projects/${snapshot.project_id}/report`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      keepalive: true,
      body: JSON.stringify({
        snapshot_id: snapshot.snapshot_id,
        content,
        recipient_class: recipient.toLowerCase().replace(" ", "-"),
        composition_depth: briefingDepth,
        included: includedBriefingSections,
        revision: draftRevision,
      }),
    }).catch(() => null);
    if (response && !response.ok) {
      setNotice("The report remains saved on this device, but workspace sync failed.");
    }
    return content;
  };

  const exportDocument = async () => {
    setNotice(null);
    await persistDocument();
    const link = document.createElement("a");
    link.href = `/api/projects/${snapshot.project_id}/export`;
    link.download = `${snapshot.project_title || "project"}-readout.pdf`;
    document.body.append(link);
    link.click();
    link.remove();
    void fetch(`/api/projects/${snapshot.project_id}/report/exports`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ format: "pdf" }),
    });
  };

  const downloadPlanFormat = (format: "excel" | "csv" | "text") => {
    const payload = buildPlanExport(snapshot)[format];
    const blob = new Blob([payload.content], { type: `${payload.mime};charset=utf-8` });
    const href = URL.createObjectURL(blob);
    const link = document.createElement("a");
    const safeTitle = projection.projectTitle
      .replace(/[<>:"/\\|?*\u0000-\u001F]+/g, "-")
      .replace(/\s+/g, " ")
      .trim() || "project";
    link.href = href;
    link.download = `${safeTitle}-plan.${payload.extension}`;
    document.body.append(link);
    link.click();
    link.remove();
    URL.revokeObjectURL(href);
    setNotice(`${format.toUpperCase()} export downloaded.`);
    void fetch(`/api/projects/${snapshot.project_id}/report/exports`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ format }),
    });
  };

  const queueDocumentSave = () => {
    if (saveTimerRef.current) window.clearTimeout(saveTimerRef.current);
    saveTimerRef.current = window.setTimeout(() => void persistDocument(), 450);
  };

  const runEditorCommand = (command: string, value?: string) => {
    editorRef.current?.focus();
    document.execCommand(command, false, value);
    void persistDocument();
  };

  const insertReportParagraph = () => {
    const editor = editorRef.current;
    if (!editor) return;

    const selection = window.getSelection();
    const anchor =
      selection?.anchorNode?.nodeType === Node.ELEMENT_NODE
        ? (selection.anchorNode as Element)
        : selection?.anchorNode?.parentElement;
    const selectedBody =
      anchor && editor.contains(anchor)
        ? anchor.closest<HTMLElement>(".report-section-body")
        : null;
    const targetBody =
      selectedBody ??
      editor.querySelector<HTMLElement>(
        '[data-section="summary"] .report-section-body',
      ) ??
      editor.querySelector<HTMLElement>(".report-section-body");
    if (!targetBody) return;

    const selectedBlock =
      anchor && targetBody.contains(anchor)
        ? anchor.closest<HTMLElement>("p, li, blockquote")
        : null;
    const paragraph = document.createElement("p");
    paragraph.append(document.createElement("br"));
    if (selectedBlock?.parentElement === targetBody) {
      selectedBlock.after(paragraph);
    } else {
      targetBody.append(paragraph);
    }

    const range = document.createRange();
    range.setStart(paragraph, 0);
    range.collapse(true);
    selection?.removeAllRanges();
    selection?.addRange(range);
    editor.focus();
    void persistDocument();
  };

  const changeRecipient = (nextRecipient: string) => {
    setRecipient(nextRecipient);
    const questions = snapshot.assessment.issues
      .filter((issue) => issue.status !== "resolved" && issue.clarification)
      .map((issue) => issue.clarification as string);
    const staging = document.createElement("div");
    staging.innerHTML = editorRef.current?.innerHTML || documentHtml;
    const decisionBody = staging.querySelector(
      '[data-section="decisions"] .report-section-body',
    );
    if (decisionBody) {
      decisionBody.innerHTML = `<p>${escapeHtml(
        audienceDecision(nextRecipient, questions),
      )}</p>`;
      const nextHtml = staging.innerHTML;
      setDocumentHtml(nextHtml);
      window.localStorage.setItem(storageKey, nextHtml);
    }
  };

  const composeBriefingSections = () => {
    const generated = buildSections(snapshot, history, recipient);
    return generated.map((section) => {
      const included =
        section.id === "summary" ||
        section.id === "changed" ||
        (section.id === "risks" && includedBriefingSections.risks) ||
        (section.id === "assumptions" && includedBriefingSections.grounding) ||
        (section.id === "action" && includedBriefingSections.moves) ||
        (section.id === "decisions" && includedBriefingSections.moves) ||
        (section.id === "appendix" && includedBriefingSections.integrity);
      if (!included) {
        return { ...section, body: ["Not included in this audience briefing."] };
      }
      return briefingDepth === "summary"
        ? { ...section, body: section.body.slice(0, 1) }
        : section;
    });
  };

  const generateDraft = () => {
    const nextHtml = sectionsToHtml(composeBriefingSections());
    const hadPreviousDraft = documentHtml !== initialHtml && documentHtml !== nextHtml;
    const nextRevision = hadPreviousDraft ? draftRevision + 1 : draftRevision;
    if (hadPreviousDraft) {
      setPreviousDocumentHtml(documentHtml);
      setDraftRevision(nextRevision);
    }
    setDocumentHtml(nextHtml);
    window.localStorage.setItem(storageKey, nextHtml);
    setBriefingStage("author");
    setNotice(
      hadPreviousDraft
        ? "Draft regenerated. Your previous authored version can still be restored."
        : "Draft generated from the current retained analysis.",
    );
    const staging = document.createElement("div");
    staging.innerHTML = nextHtml;
    void fetch(`/api/projects/${snapshot.project_id}/report`, {
      method: "PUT",
      headers: { "content-type": "application/json" },
      keepalive: true,
      body: JSON.stringify({
        snapshot_id: snapshot.snapshot_id,
        content: editorContent(staging, initialSections),
        recipient_class: recipient.toLowerCase().replace(" ", "-"),
        composition_depth: briefingDepth,
        included: includedBriefingSections,
        revision: nextRevision,
      }),
    }).then((response) => {
      if (!response.ok) {
        setNotice("The draft remains saved on this device, but workspace sync failed.");
      }
    }).catch(() => {
      setNotice("The draft remains saved on this device, but workspace sync failed.");
    });
  };

  const createWeeklySchedule = async () => {
    const normalizedEmail = deliveryEmail.trim();
    const emailValidator = document.createElement("input");
    emailValidator.type = "email";
    emailValidator.required = true;
    emailValidator.value = normalizedEmail;
    if (!emailValidator.checkValidity()) {
      setNotice("Enter a valid recipient email address.");
      return;
    }
    setDeliveryPending(true);
    setNotice(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/report/schedules`,
        {
          method: "POST",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({
            recipient_email: normalizedEmail,
            recipient_class: recipient.toLowerCase().replace(" ", "-"),
            weekday: Number(weeklyDay),
            local_time: `${weeklyTime}:00`,
            timezone: weeklyTimezone,
          }),
        },
      );
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(
          response.status === 402
            ? "Weekly delivery requires Basic. Send now and manual exports remain free."
            : result.message || "Weekly delivery could not be scheduled.",
        );
      }
      setNotice(
        `Weekly delivery scheduled. Next send: ${reportDateTimeFormatter.format(
          new Date(result.next_run_at),
        )} UTC.`,
      );
      setReportSchedules((current) => [
        result as ReportSchedule,
        ...current.filter((schedule) => schedule.id !== result.id),
      ]);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Weekly delivery could not be scheduled.");
    } finally {
      setDeliveryPending(false);
    }
  };

  const changeScheduleState = async (
    schedule: ReportSchedule,
    state: "enabled" | "paused",
  ) => {
    setScheduleActionId(schedule.id);
    setNotice(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/report/schedules/${schedule.id}`,
        {
          method: "PATCH",
          headers: { "content-type": "application/json" },
          body: JSON.stringify({ state }),
        },
      );
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.message || "Schedule could not be updated.");
      setReportSchedules((current) =>
        current.map((item) => (item.id === schedule.id ? result : item)),
      );
      setNotice(state === "paused" ? "Weekly delivery paused." : "Weekly delivery resumed.");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Schedule could not be updated.");
    } finally {
      setScheduleActionId(null);
    }
  };

  const removeSchedule = async (schedule: ReportSchedule) => {
    setScheduleActionId(schedule.id);
    setNotice(null);
    try {
      const response = await fetch(
        `/api/projects/${snapshot.project_id}/report/schedules/${schedule.id}`,
        { method: "DELETE" },
      );
      if (!response.ok) {
        const result = await response.json().catch(() => ({}));
        throw new Error(result.message || "Schedule could not be removed.");
      }
      setReportSchedules((current) => current.filter((item) => item.id !== schedule.id));
      setNotice("Weekly delivery removed.");
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Schedule could not be removed.");
    } finally {
      setScheduleActionId(null);
    }
  };

  const copySummary = async () => {
    try {
      await navigator.clipboard.writeText(projection.summary);
      setNotice("Summary copied to the clipboard.");
    } catch {
      const textarea = document.createElement("textarea");
      textarea.value = projection.summary;
      textarea.style.position = "fixed";
      textarea.style.opacity = "0";
      document.body.append(textarea);
      textarea.select();
      const copied = document.execCommand("copy");
      textarea.remove();
      setNotice(copied ? "Summary copied to the clipboard." : "Copy failed. Select the summary and try again.");
    }
    void fetch(`/api/projects/${snapshot.project_id}/report/exports`, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ format: "copy-summary" }),
    });
  };

  const importToAsana = async () => {
    if (!asanaState?.entitled) {
      setNotice("Asana hand-off requires Basic. Manual exports remain free.");
      setExportOpen(false);
      return;
    }
    if (!asanaState.configured) {
      setNotice(
        "Connect an Asana project in workspace settings before importing. Manual exports remain available.",
      );
      setExportOpen(false);
      return;
    }
    setAsanaPending(true);
    setNotice(null);
    try {
      const response = await fetch(`/api/projects/${snapshot.project_id}/report/asana`, {
        method: "POST",
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(result.message || "Asana import failed safely.");
      setAsanaState((current) => (current ? { ...current, latest: result } : current));
      setNotice(
        result.state === "completed"
          ? `${result.completed_count} executable plan items imported to Asana.`
          : `${result.completed_count} of ${result.total_count} items imported. Retry to resume safely.`,
      );
      setExportOpen(false);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Asana import failed safely.");
    } finally {
      setAsanaPending(false);
    }
  };

  const deliver = async (schedule: string | null) => {
    const normalizedEmail = deliveryEmail.trim();
    const emailValidator = document.createElement("input");
    emailValidator.type = "email";
    emailValidator.required = true;
    emailValidator.value = normalizedEmail;
    if (!emailValidator.checkValidity()) {
      setNotice("Enter a valid recipient email address.");
      return;
    }
    if (isPreviousAnalysis) {
      setNotice(
        "Refresh the report from the current analysis before sending or scheduling it.",
      );
      return;
    }
    setDeliveryPending(true);
    setNotice(null);
    try {
      let latestSnapshotId = currentSnapshotId;
      const currencyResponse = await fetch(
        `/api/projects/${snapshot.project_id}/report`,
        { cache: "no-store" },
      ).catch(() => null);
      if (currencyResponse?.ok) {
        const currency = (await currencyResponse.json()) as { snapshot_id: string };
        latestSnapshotId = currency.snapshot_id;
        setCurrentSnapshotId(currency.snapshot_id);
      }
      const sendingPreviousAnalysis = latestSnapshotId !== snapshot.snapshot_id;
      if (sendingPreviousAnalysis) {
        setNotice(
          "Refresh the report from the current analysis before sending or scheduling it.",
        );
        return;
      }
      const content = await persistDocument();
      const response = await fetch(`/api/projects/${snapshot.project_id}/report`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({
          snapshot_id: snapshot.snapshot_id,
          recipient_email: normalizedEmail,
          recipient_label: recipient,
          subject: `${snapshot.project_title || "Project"} readout`,
          content,
          scheduled_for: schedule,
          confirm_previous_analysis: false,
        }),
      });
      const result = await response.json().catch(() => ({}));
      if (!response.ok) {
        throw new Error(result.message || "Report delivery failed.");
      }
      if (result.status === "failed") {
        throw new Error(
          "The report was saved, but email delivery failed. Check the mail service and retry.",
        );
      }
      setNotice(
        result.status === "sent"
          ? `Report emailed to ${normalizedEmail}.`
          : `Report scheduled for ${reportDateTimeFormatter.format(new Date(result.scheduled_for))} UTC.`,
      );
      setDeliveries((current) => [result as ReportDelivery, ...current]);
      if (result.status === "sent") setBriefingStage("sent");
      setSendOpen(false);
      setScheduleOpen(false);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Report delivery failed.");
    } finally {
      setDeliveryPending(false);
    }
  };

  return (
    <section className="report-workspace">
      <p aria-label="Reports location" className="report-breadcrumb">
        <span>Outcome</span>
        <CaretRight aria-hidden="true" size={10} />
        <strong>Reports</strong>
      </p>
      {showReportWelcome ? (
        <section aria-label="Reports welcome" className="report-welcome">
          <Sparkle aria-hidden="true" size={18} weight="fill" />
          <div>
            <strong>Your outcome view is open.</strong>
            <p>
              Your governed read is ready to shape into an authored briefing or a read-only
              snapshot. Reports never change the analysis behind them.
            </p>
            <div>
              <small>New to OSLO?</small>
              <button
                onClick={() => {
                  setNotice("Start with Executive Briefing to author a memo, or open a generated report for a read-only snapshot.");
                  reportTabRefs.current[0]?.focus();
                }}
                type="button"
              >
                Take a 30-second tour →
              </button>
              <button
                onClick={() => {
                  window.localStorage.setItem(reportWelcomeKey, "dismissed");
                  setShowReportWelcome(false);
                }}
                type="button"
              >
                No thanks
              </button>
            </div>
          </div>
          <button
            aria-label="Dismiss reports welcome"
            onClick={() => {
              window.localStorage.setItem(reportWelcomeKey, "dismissed");
              setShowReportWelcome(false);
            }}
            type="button"
          >
            <X aria-hidden="true" size={14} />
          </button>
        </section>
      ) : null}
      <header className="report-heading">
        <h1>Reports</h1>
        <p>The readout — a projection; produces no new assessment.</p>
      </header>
      <nav aria-label="Reports" className="report-view-tabs" role="tablist">
        {reportViews.map((view, index) => (
          <button
            aria-controls={`report-panel-${view.id}`}
            aria-selected={activeReport === view.id}
            className={activeReport === view.id ? "is-active" : undefined}
            id={`report-tab-${view.id}`}
            key={view.id}
            onClick={() => setActiveReport(view.id)}
            onKeyDown={(event) => {
              if (!["ArrowLeft", "ArrowRight", "Home", "End"].includes(event.key)) return;
              event.preventDefault();
              const nextIndex = event.key === "Home"
                ? 0
                : event.key === "End"
                  ? reportViews.length - 1
                  : (index + (event.key === "ArrowRight" ? 1 : -1) + reportViews.length)
                    % reportViews.length;
              const nextView = reportViews[nextIndex];
              setActiveReport(nextView.id);
              reportTabRefs.current[nextIndex]?.focus();
            }}
            ref={(element) => {
              reportTabRefs.current[index] = element;
            }}
            role="tab"
            tabIndex={activeReport === view.id ? 0 : -1}
            type="button"
          >
            <span>{view.ownership}</span>
            {" "}{view.name}
          </button>
        ))}
      </nav>
      <div
        aria-labelledby={`report-tab-${activeReport}`}
        id={`report-panel-${activeReport}`}
        role="tabpanel"
      >
      {activeReport === "executive-briefing" ? (
      <>
      <p className="report-view-context">The note that goes out — composed, and yours to edit.</p>
      <aside className="briefing-analysis-currency" role="note">
        <strong>Current analysis</strong>
        <span>
          Dated to the analysis behind it — {reportDateTimeFormatter.format(new Date(projection.analysisAt))} UTC,
          not the moment you export.
        </span>
      </aside>
      <nav aria-label="Executive Briefing progress" className="briefing-lifecycle">
        <button
          aria-current={briefingStage === "compose" ? "step" : undefined}
          className={briefingStage !== "compose" ? "is-complete" : undefined}
          onClick={() => setBriefingStage("compose")}
          type="button"
        >
          <span>1</span> Generate
        </button>
        <button
          aria-current={briefingStage === "author" ? "step" : undefined}
          className={briefingStage === "sent" ? "is-complete" : undefined}
          disabled={briefingStage === "compose"}
          onClick={() => setBriefingStage("author")}
          type="button"
        >
          <span>2</span> Author
        </button>
        <button
          aria-current={briefingStage === "sent" ? "step" : undefined}
          disabled={briefingStage === "compose"}
          onClick={() => setSendOpen(true)}
          type="button"
        >
          <span>3</span> Send
        </button>
      </nav>
      {briefingStage === "compose" ? (
        <section className="briefing-compose" aria-labelledby="briefing-compose-title">
          <h1 className="sr-only" id="briefing-compose-title">Compose an Executive Briefing</h1>
          {notice ? <p className="report-notice" role="status">{notice}</p> : null}
          <div className="briefing-compose-row">
            <span>For</span>
            <div aria-label="Briefing recipient" role="group">
              {["Exec sponsor", "Team", "Board"].map((option) => (
                <button
                  aria-pressed={recipient === option}
                  key={option}
                  onClick={() => changeRecipient(option)}
                  type="button"
                >
                  {option}
                </button>
              ))}
            </div>
          </div>
          <div className="briefing-compose-row">
            <span>Depth</span>
            <div aria-label="Briefing depth" role="group">
              {(["summary", "full"] as const).map((depth) => (
                <button
                  aria-pressed={briefingDepth === depth}
                  key={depth}
                  onClick={() => setBriefingDepth(depth)}
                  type="button"
                >
                  {depth === "summary" ? "Summary" : "Full"}
                </button>
              ))}
            </div>
          </div>
          <div className="briefing-compose-row">
            <span>Include</span>
            <div aria-label="Briefing sections" role="group">
              {([
                ["integrity", "Integrity"],
                ["risks", "Top risks"],
                ["grounding", "What’s grounded"],
                ["moves", "Next moves"],
              ] as const).map(([key, label]) => (
                <button
                  aria-pressed={includedBriefingSections[key]}
                  key={key}
                  onClick={() => setIncludedBriefingSections((current) => ({
                    ...current,
                    [key]: !current[key],
                  }))}
                  type="button"
                >
                  {includedBriefingSections[key] ? <Check aria-hidden="true" size={12} /> : null}
                  {label}
                </button>
              ))}
            </div>
          </div>
          <div className="briefing-compose-row">
            <span>Deliver</span>
            <div>
              <button
                className="briefing-basic-gate"
                onClick={() => {
                  generateDraft();
                  setScheduleOpen(true);
                }}
                type="button"
              >
                <Clock aria-hidden="true" size={12} /> Send on a schedule <LockSimple aria-hidden="true" size={11} /> Basic
              </button>
              <small>Send now stays free. Weekly delivery re-reads for currency before every send.</small>
            </div>
          </div>
          <div className="briefing-compose-action">
            <button
              onClick={generateDraft}
              type="button"
            >
              <Sparkle aria-hidden="true" size={12} /> Generate a draft →
            </button>
            <span>OSLO drafts it from your governed read — then it’s yours to author, in your own words.</span>
          </div>
          <p className="briefing-compose-footnote">
            One plan, served many ways — you author the report; the memo is the immutable copy that travels.
          </p>
        </section>
      ) : briefingStage === "sent" ? (
        <section className="briefing-sent" aria-labelledby="briefing-sent-title">
          {notice ? <p className="report-notice" role="status">{notice}</p> : null}
          <strong>✓ Sent</strong>
          <h1 id="briefing-sent-title">Immutable memo package</h1>
          <p>A dated snapshot left OSLO. Your living report remains available to edit and send again.</p>
          <article>
            <header>
              <span>
                Memo {deliveries[0]?.report_version ?? 1} · {deliveries[0]?.recipient_label ?? recipient}
              </span>
              <strong>
                {reportDateTimeFormatter.format(
                  new Date(
                    deliveries[0]?.sent_at ??
                      deliveries[0]?.scheduled_for ??
                      projection.analysisAt,
                  ),
                )} UTC
              </strong>
            </header>
            <p className="briefing-sent-disclaimer">
              This memo is a projection of a governed plan read — a maturity read, not a probability of success.
              OSLO advises; the sender decides.
            </p>
            <div className="briefing-sent-document" dangerouslySetInnerHTML={{ __html: documentHtml }} />
          </article>
          <div className="briefing-sent-actions">
            <button onClick={() => setBriefingStage("author")} type="button">Back to report</button>
            <button onClick={() => setExportOpen(true)} type="button">Export memo</button>
          </div>
          {deliveries.length > 1 ? (
            <section aria-label="Previous memo versions" className="briefing-memo-versions">
              <h2>Previous memos</h2>
              {deliveries.slice(1).map((delivery) => (
                <article key={delivery.id}>
                  <strong>Memo {delivery.report_version}</strong>
                  <span>
                    {delivery.recipient_label} · {delivery.currency_state === "current" ? "Current analysis" : "Previous analysis"}
                  </span>
                  <time dateTime={delivery.sent_at ?? delivery.scheduled_for}>
                    {reportDateTimeFormatter.format(new Date(delivery.sent_at ?? delivery.scheduled_for))} UTC
                  </time>
                </article>
              ))}
            </section>
          ) : null}
        </section>
      ) : (
      <>
      <div className="briefing-author-actions">
        <span>For <strong>{recipient}</strong> · {briefingDepth === "full" ? "Full" : "Summary"}</span>
        <button onClick={() => setBriefingStage("compose")} type="button">↻ Start over</button>
        {previousDocumentHtml ? (
          <button
            onClick={() => {
              setDocumentHtml(previousDocumentHtml);
              window.localStorage.setItem(storageKey, previousDocumentHtml);
              setPreviousDocumentHtml(null);
              setNotice("Previous authored version restored.");
            }}
            type="button"
          >
            Restore previous version
          </button>
        ) : null}
      </div>
      <div className="briefing-author-intro">
        <strong>Your report — authored by you</strong>
        <span>Living document · tracks the read</span>
        <p>OSLO drafted this from the read; now it’s yours to write. Edit it in your own voice, for your reader.</p>
      </div>
      <header aria-label="Readout controls" className="report-toolbar" role="toolbar">
        <strong className="report-toolbar-name">Readout</strong>
        <div aria-label="Editor actions" className="report-editor-actions">
          <button aria-label="Undo" onClick={() => runEditorCommand("undo")} type="button">
            <ArrowCounterClockwise size={14} />
          </button>
          <button aria-label="Redo" onClick={() => runEditorCommand("redo")} type="button">
            <ArrowClockwise size={14} />
          </button>
          <button
            aria-label="Insert paragraph"
            onClick={insertReportParagraph}
            type="button"
          >
            <Plus size={14} />
          </button>
          <button
            aria-expanded={findOpen}
            aria-label="Find in readout"
            onClick={() => setFindOpen((current) => !current)}
            type="button"
          >
            <MagnifyingGlass size={14} />
          </button>
          <span aria-hidden="true" />
          <button aria-label="Bold" onClick={() => runEditorCommand("bold")} type="button">
            <TextB size={14} />
          </button>
          <button aria-label="Italic" onClick={() => runEditorCommand("italic")} type="button">
            <TextItalic size={14} />
          </button>
          <button aria-label="Underline" onClick={() => runEditorCommand("underline")} type="button">
            <TextUnderline size={14} />
          </button>
          <button
            aria-label="Bulleted list"
            onClick={() => runEditorCommand("insertUnorderedList")}
            type="button"
          >
            <ListBullets size={14} />
          </button>
          <button
            aria-label="Add link"
            onClick={() => runEditorCommand("createLink", "https://")}
            type="button"
          >
            <LinkSimple size={14} />
          </button>
        </div>

        <div className="report-toolbar-spacer" />

        <label className="report-recipient-control">
          <span>Recipient</span>
          <select
            aria-label="Report recipient"
            onChange={(event) => changeRecipient(event.target.value)}
            value={recipient}
          >
            <option>Exec sponsor</option>
            <option>Team</option>
            <option>Board</option>
          </select>
        </label>

        <div className="report-toolbar-menu">
          <button
            aria-expanded={sectionsOpen}
            onClick={() => {
              setSectionsOpen((current) => !current);
              setScheduleOpen(false);
            }}
            type="button"
          >
            Sections <CaretDown size={11} />
          </button>
          {sectionsOpen ? (
            <div aria-label="Readout sections" role="menu">
              {reportSectionOrder.map((id) => {
                const section = initialSections.find((item) => item.id === id)!;
                return (
                  <button
                    key={id}
                    onClick={() => {
                      editorRef.current
                        ?.querySelector(`[data-section="${id}"]`)
                        ?.scrollIntoView({ behavior: "smooth", block: "start" });
                      setSectionsOpen(false);
                    }}
                    role="menuitem"
                    type="button"
                  >
                    {section.title}
                  </button>
                );
              })}
            </div>
          ) : null}
        </div>

        <span className="report-format-control">Format&nbsp; PDF</span>

        <div className="report-toolbar-menu">
          <button
            aria-expanded={scheduleOpen}
            onClick={() => {
              if (isPreviousAnalysis) {
                setNotice(
                  "Refresh the report from the current analysis before sending or scheduling it.",
                );
                setScheduleOpen(false);
                return;
              }
              setScheduleOpen((current) => !current);
              setSectionsOpen(false);
            }}
            type="button"
          >
            Schedule <CaretDown size={11} />
          </button>
          {scheduleOpen ? (
            <div aria-label="Readout schedule" className="report-delivery-panel">
              <label>
                Recipient email
                <input
                  onChange={(event) => setDeliveryEmail(event.target.value)}
                  placeholder="sponsor@example.com"
                  type="email"
                  value={deliveryEmail}
                />
              </label>
              <label>
                Day
                <select onChange={(event) => setWeeklyDay(event.target.value)} value={weeklyDay}>
                  <option value="0">Monday</option>
                  <option value="1">Tuesday</option>
                  <option value="2">Wednesday</option>
                  <option value="3">Thursday</option>
                  <option value="4">Friday</option>
                  <option value="5">Saturday</option>
                  <option value="6">Sunday</option>
                </select>
              </label>
              <label>
                Local time
                <input
                  onChange={(event) => setWeeklyTime(event.target.value)}
                  type="time"
                  value={weeklyTime}
                />
              </label>
              <label>
                Timezone
                <input
                  onChange={(event) => setWeeklyTimezone(event.target.value)}
                  value={weeklyTimezone}
                />
              </label>
              <button
                disabled={deliveryPending || !deliveryEmail.trim() || !weeklyTime || !weeklyTimezone}
                onClick={() => void createWeeklySchedule()}
                type="button"
              >
                {deliveryPending ? "Scheduling…" : "Schedule weekly · Basic"}
              </button>
              <small>
                OSLO checks that the authored report still matches the current analysis before every send.
              </small>
              {reportSchedules.length ? (
                <section aria-label="Existing weekly schedules" className="report-schedule-list">
                  <strong>Weekly schedules</strong>
                  {reportSchedules.map((schedule) => (
                    <article key={schedule.id}>
                      <div>
                        <span>
                          {reportWeekdays[schedule.weekday]} at {schedule.local_time.slice(0, 5)} · {schedule.timezone}
                        </span>
                        <strong>{schedule.recipient_email}</strong>
                        <small>
                          {schedule.state === "enabled"
                            ? `Next ${reportDateTimeFormatter.format(new Date(schedule.next_run_at))} UTC`
                            : "Paused"}
                        </small>
                      </div>
                      <div>
                        <button
                          aria-label={`${schedule.state === "enabled" ? "Pause" : "Resume"} weekly schedule for ${schedule.recipient_email}`}
                          disabled={scheduleActionId === schedule.id}
                          onClick={() =>
                            void changeScheduleState(
                              schedule,
                              schedule.state === "enabled" ? "paused" : "enabled",
                            )
                          }
                          type="button"
                        >
                          {schedule.state === "enabled" ? "Pause" : "Resume"}
                        </button>
                        <button
                          aria-label={`Remove weekly schedule for ${schedule.recipient_email}`}
                          disabled={scheduleActionId === schedule.id}
                          onClick={() => void removeSchedule(schedule)}
                          type="button"
                        >
                          Remove
                        </button>
                      </div>
                    </article>
                  ))}
                </section>
              ) : null}
            </div>
          ) : null}
        </div>

        <button
          className="report-send"
          onClick={() => {
            if (isPreviousAnalysis) {
              setNotice(
                "Refresh the report from the current analysis before sending or scheduling it.",
              );
              setSendOpen(false);
              return;
            }
            setSendOpen((current) => !current);
            setExportOpen(false);
            setEditingRecipient(false);
            setScheduleOpen(false);
            setSectionsOpen(false);
          }}
          aria-expanded={sendOpen}
          type="button"
        >
          <EnvelopeSimple size={14} /> Send <CaretDown size={10} />
        </button>
        <button
          aria-expanded={exportOpen}
          className="report-export"
          onClick={() => {
            setExportOpen((current) => !current);
            setSendOpen(false);
            setScheduleOpen(false);
            setSectionsOpen(false);
          }}
          type="button"
        >
          <DownloadSimple size={14} /> Export
        </button>
      </header>

      {sendOpen ? (
        <div aria-label="Send readout" className="report-send-panel" role="dialog">
          <span className="report-popover-label">Send</span>
          <p>Goes to <strong>{recipient}</strong> as a read-only copy, on a link back into OSLO.</p>
          <div className="report-send-actions">
            <button
              aria-label={`Send to the ${recipient.toLowerCase()}`}
              className="is-primary"
              disabled={deliveryPending || !deliveryEmail.trim()}
              onClick={() => void deliver(null)}
              type="button"
            >
              {deliveryPending ? "Sending…" : `→ Send to the ${recipient.toLowerCase()}`}
            </button>
            <button onClick={() => setEditingRecipient((current) => !current)} type="button">
              Change recipient
            </button>
          </div>
          {editingRecipient || !deliveryEmail.trim() ? (
            <label>
              Recipient email
              <input
                autoFocus
                onChange={(event) => setDeliveryEmail(event.target.value)}
                placeholder="sponsor@example.com"
                type="email"
                value={deliveryEmail}
              />
            </label>
          ) : null}
          <p>Sending runs no analysis. It writes down the read you already have.</p>
          <p>The link is their access — <strong>no signup</strong>. It opens this one memo, read-only, and nothing else.</p>
          <strong>Free on every plan.</strong>
        </div>
      ) : null}

      {exportOpen ? createPortal((
        <div className="report-modal-backdrop" onMouseDown={() => setExportOpen(false)}>
        <div
          aria-label="Export your plan"
          aria-modal="true"
          className="report-export-panel"
          onMouseDown={(event) => event.stopPropagation()}
          ref={exportDialogRef}
          role="dialog"
        >
          <header>
            <div>
              <span className="report-popover-label">Export your plan</span>
              <p>
                <strong>{projection.projectTitle}</strong> · {asanaState
                  ? `${asanaState.preview.length} ${asanaState.preview.length === 1 ? "task" : "tasks"}`
                  : "executable plan"} · {projection.integrity.level}
              </p>
            </div>
            <div className="report-export-header-actions">
              <button aria-expanded={exportDetailsOpen} onClick={() => setExportDetailsOpen((current) => !current)} type="button">
                Details
              </button>
              <button aria-label="Close export" onClick={() => setExportOpen(false)} type="button">×</button>
            </div>
          </header>
          {exportDetailsOpen ? (
            <aside className="report-export-details" role="note">
              <span>Optimized for the current outcome</span>
              <strong>{projection.criticalGrounding.grounded} of {projection.criticalGrounding.total} critical details grounded</strong>
              <p>Exports executable plan fields and provenance. Hidden reasoning is excluded.</p>
            </aside>
          ) : null}
          <span className="report-popover-label">Choose a format</span>
          <div aria-label="Export format" className="report-export-formats" role="group">
            {([['excel', 'Excel'], ['csv', 'CSV'], ['text', 'Text'], ['pdf', 'PDF package']] as const).map(([format, label]) => (
              <button aria-pressed={exportFormat === format} key={format} onClick={() => setExportFormat(format)} type="button">
                {label}
              </button>
            ))}
          </div>
          <p>A dated snapshot with the advisory disclaimer and retained analysis time.</p>
          <div className="report-export-actions">
            <button
              className="is-primary"
              onClick={() => exportFormat === "pdf" ? void exportDocument() : downloadPlanFormat(exportFormat)}
              type="button"
            >
              <DownloadSimple size={14} /> {exportFormat === "pdf" ? "Export as PDF" : `Download the ${exportFormat.toUpperCase()}`}
            </button>
            <button onClick={() => void copySummary()} type="button">
              Copy summary
            </button>
            <button onClick={() => setExportOpen(false)} type="button">Cancel</button>
          </div>
          <div className="report-asana-gate">
            <div>
              <strong>Or let OSLO import it into Asana for you</strong>
              <span>
                One-way · executable plan fields only
                {asanaState?.preview.length ? ` · ${asanaState.preview.length} ready` : ""}
              </span>
              {asanaState?.latest ? (
                <small>
                  Last hand-off: {asanaState.latest.completed_count} of {asanaState.latest.total_count} · {asanaState.latest.state}
                </small>
              ) : null}
            </div>
            <button disabled={asanaPending} onClick={() => void importToAsana()} type="button">
              {asanaPending
                ? "Importing…"
                : !asanaState?.entitled
                  ? "Upgrade to Basic →"
                  : !asanaState.configured
                    ? "Connect Asana →"
                    : `Import ${asanaState.preview.length} tasks →`}
            </button>
          </div>
          <footer>Carries OSLO’s advisory disclaimer — a read of the plan’s maturity, not a forecast.</footer>
          <p>A memo is frozen when it goes. If the read moves on, it remains a labelled previous analysis.</p>
        </div>
        </div>
      ), document.body) : null}

      {findOpen ? (
        <div className="report-find" role="search">
          <MagnifyingGlass size={14} />
          <input
            autoFocus
            onChange={(event) => {
              const value = event.target.value;
              const needle = value.trim().toLowerCase();
              setFindValue(value);
              setFindCount(
                needle
                  ? (editorRef.current?.innerText.toLowerCase().split(needle).length ?? 1) - 1
                  : 0,
              );
            }}
            placeholder="Find in readout"
            value={findValue}
          />
          <span>{findValue ? `${findCount} found` : "Type to find"}</span>
        </div>
      ) : null}

      {notice ? <p className="report-notice" role="status">{notice}</p> : null}

      {isPreviousAnalysis ? (
        <aside className="report-currency-warning" role="note">
          <strong>Previous analysis</strong>
          <span>
            This retained report does not include the latest project analysis.
            Refresh it from the current analysis before sending or scheduling.
          </span>
        </aside>
      ) : null}

      <article className="report-document">
        <header>
          <h1>{snapshot.project_title || "Project understanding"}</h1>
          <span>
            Plan as of {reportDateFormatter.format(new Date(snapshot.published_at))} {"\u00b7"} Prepared for {recipient}
          </span>
          <span>To: {recipient}</span>
        </header>
        <div
          aria-label="Edit readout"
          aria-multiline="true"
          className="report-continuous-editor"
          contentEditable
          dangerouslySetInnerHTML={{ __html: documentHtml }}
          key={`${currentSnapshotId}:${documentHtml}`}
          onBlur={persistDocument}
          onInput={queueDocumentSave}
          ref={editorRef}
          role="textbox"
          suppressContentEditableWarning
        />
        <footer>
          <span>Saved automatically to this workspace</span>
          <span>
            {isPreviousAnalysis
              ? "This document reflects a previous retained project analysis."
              : "This document reflects the current retained project analysis."}
          </span>
        </footer>
      </article>
      </>
      )}
      </>
      ) : (
        <>
          {notice ? <p className="report-notice" role="status">{notice}</p> : null}
          <GeneratedReportView
            onExport={() => downloadPlanFormat("text")}
            projection={projection}
            view={activeReport}
          />
        </>
      )}
      </div>
    </section>
  );
}
