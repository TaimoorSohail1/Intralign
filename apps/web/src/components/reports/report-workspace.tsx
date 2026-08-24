"use client";

import {
  ArrowCounterClockwise,
  ArrowClockwise,
  CaretDown,
  DownloadSimple,
  EnvelopeSimple,
  LinkSimple,
  ListBullets,
  MagnifyingGlass,
  Plus,
  TextB,
  TextItalic,
  TextUnderline,
} from "@phosphor-icons/react";
import { useEffect, useMemo, useRef, useState } from "react";

import type { OverviewSnapshot, ProjectHistory, ReportContent } from "@/lib/server/oslo-api";

type ReportSection = {
  id: string;
  title: string;
  body: string[];
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

function localDateTimeValue(value: Date) {
  const offset = value.getTimezoneOffset() * 60_000;
  return new Date(value.getTime() - offset).toISOString().slice(0, 16);
}

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
  if (recipient === "Delivery team") {
    return `Please confirm the delivery owner and next practical step: ${openQuestion}`;
  }
  if (recipient === "Steering group") {
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
          snapshot.summary,
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
  const defaultRecipient = "Sponsor";
  const initialSections = useMemo(
    () => buildSections(snapshot, history, defaultRecipient),
    [history, snapshot],
  );
  const storageKey = `oslo:readout:${snapshot.project_id}:${snapshot.snapshot_id}`;
  const initialHtml = useMemo(() => sectionsToHtml(initialSections), [initialSections]);
  const editorRef = useRef<HTMLDivElement>(null);
  const saveTimerRef = useRef<number | null>(null);
  const [sectionsOpen, setSectionsOpen] = useState(false);
  const [scheduleOpen, setScheduleOpen] = useState(false);
  const [findOpen, setFindOpen] = useState(false);
  const [findValue, setFindValue] = useState("");
  const [findCount, setFindCount] = useState(0);
  const [recipient, setRecipient] = useState(defaultRecipient);
  const [notice, setNotice] = useState<string | null>(null);
  const [sendOpen, setSendOpen] = useState(false);
  const [exportOpen, setExportOpen] = useState(false);
  const [editingRecipient, setEditingRecipient] = useState(false);
  const [deliveryEmail, setDeliveryEmail] = useState("sponsor@example.com");
  const [scheduledFor, setScheduledFor] = useState("");
  const [deliveryPending, setDeliveryPending] = useState(false);
  const [documentHtml, setDocumentHtml] = useState(initialHtml);
  const [currentSnapshotId, setCurrentSnapshotId] = useState(snapshot.snapshot_id);
  const isPreviousAnalysis = currentSnapshotId !== snapshot.snapshot_id;

  useEffect(() => {
    let active = true;
    const loadSharedDraft = async () => {
      const deviceHtml = sanitizeReadoutHtml(
        window.localStorage.getItem(storageKey) || "",
      );
      if (deviceHtml) setDocumentHtml(deviceHtml);
      try {
        const response = await fetch(`/api/projects/${snapshot.project_id}/report`);
        if (!response.ok) return;
        const result = (await response.json()) as {
          snapshot_id: string;
          content: ReportContent | null;
        };
        setCurrentSnapshotId(result.snapshot_id);
        if (!active || result.snapshot_id !== snapshot.snapshot_id) return;
        if (result.content) {
          const html = contentToHtml(result.content);
          setDocumentHtml(html);
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
            <option>Sponsor</option>
            <option>Steering group</option>
            <option>Delivery team</option>
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
                Delivery time
                <input
                  min={localDateTimeValue(new Date())}
                  onChange={(event) => setScheduledFor(event.target.value)}
                  onInput={(event) =>
                    setScheduledFor((event.target as HTMLInputElement).value)
                  }
                  type="datetime-local"
                  value={scheduledFor}
                />
              </label>
              <button
                disabled={deliveryPending || !scheduledFor}
                onClick={() => void deliver(new Date(scheduledFor).toISOString())}
                type="button"
              >
                {deliveryPending ? "Scheduling…" : "Schedule delivery"}
              </button>
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
              disabled={deliveryPending}
              onClick={() => void deliver(null)}
              type="button"
            >
              {deliveryPending ? "Sending…" : `→ Send to the ${recipient.toLowerCase()}`}
            </button>
            <button onClick={() => setEditingRecipient((current) => !current)} type="button">
              Change recipient
            </button>
          </div>
          {editingRecipient ? (
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

      {exportOpen ? (
        <div aria-label="Export readout" className="report-export-panel" role="dialog">
          <span className="report-popover-label">Export</span>
          <div className="report-export-actions">
            <button className="is-primary" onClick={() => void exportDocument()} type="button">
              <DownloadSimple size={14} /> Export as PDF
            </button>
            <button type="button">Change format</button>
            <button type="button">Preview what travels</button>
          </div>
          <p>A file you handle yourself. To send it to someone, use Send.</p>
          <hr />
          <span className="report-popover-label">Memos</span>
          <article>
            <p><strong>Memo 1</strong> <span>Current analysis</span></p>
            <small>Frozen when exported · prepared for {recipient}</small>
          </article>
          <p>A memo is frozen when it goes. If the read moves on, it remains a labelled previous analysis.</p>
        </div>
      ) : null}

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
    </section>
  );
}
