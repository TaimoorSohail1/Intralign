import Link from "next/link";
import { Check } from "@phosphor-icons/react";
import type { CSSProperties } from "react";

import type {
  CollaborationRollUpProjection,
  GroundingMapProjection,
  GroundingNodeState,
} from "@/lib/server/oslo-api";

const stateLabels: Record<GroundingNodeState, string> = {
  grounded: "Grounded",
  addressed: "Addressed · analysis pending",
  routed: "Routed · awaiting evidence",
  inferred: "Inferred",
};

const groundingLegendLabels: Record<GroundingNodeState, string> = {
  grounded: "Grounded — yours, on your evidence",
  addressed: "Addressed — analysis pending",
  routed: "Routed — awaiting evidence",
  inferred: "Still OSLO’s inference",
};

type GroundingPlacement = CSSProperties & {
  "--node-angle": string;
  "--orbit-radius": string;
};

function groundingPlacement(index: number, total: number) {
  const dense = total > 8;
  const angle = -90 + (360 / Math.max(total, 1)) * index;
  const radians = (angle * Math.PI) / 180;
  const horizontal = Math.cos(radians);
  const vertical = Math.sin(radians);
  const nearVertical = Math.abs(horizontal) < 0.12;
  const labelPosition = nearVertical && vertical < 0
    ? "label-top"
    : nearVertical && vertical > 0
      ? "label-bottom"
      : horizontal < 0
        ? "label-left"
        : "label-right";

  return {
    labelPosition,
    style: {
      "--node-angle": `${angle}deg`,
      "--orbit-radius": dense ? "220px" : "174px",
    } as GroundingPlacement,
  };
}

export function CollaborationRollUp({ data }: { data: CollaborationRollUpProjection }) {
  const answeredReviews = data.who_is_grounding_what.filter(
    (item) => item.state === "answered",
  ).length;
  const reviewSummary = answeredReviews
    ? `${answeredReviews} answered${answeredReviews < data.who_is_grounding_what.length ? ` · ${data.who_is_grounding_what.length - answeredReviews} awaiting` : ""}`
    : `${data.who_is_grounding_what.length} routed`;

  return (
    <section className="collaboration-projection" aria-labelledby="roll-up-title">
      <header className="collaboration-projection-heading">
        <div>
          <span>Owner roll-up · read only</span>
          <h1 id="roll-up-title">What needs your judgment</h1>
          <p>One projection over the current read. Open a row to act from its issue.</p>
        </div>
        <strong>{data.integrity.level}</strong>
      </header>

      <div className="collaboration-rollup-grid">
        <article>
          <small>Weakest gate</small>
          <strong>{data.integrity.limiting_pillar}</strong>
          <span>{data.trend === "unchanged" ? "No movement yet" : data.trend}</span>
        </article>
        {Object.entries(data.rests_on).map(([state, count]) => (
          <article key={state}>
            <small>{stateLabels[state as GroundingNodeState]}</small>
            <strong>{count}</strong>
            <span>load-bearing item{count === 1 ? "" : "s"}</span>
          </article>
        ))}
      </div>

      <section className="collaboration-projection-list" aria-labelledby="decision-queue-title">
        <header>
          <div>
            <span>Decision queue</span>
            <h2 id="decision-queue-title">Most important first</h2>
          </div>
          <small>{data.decision_queue.length} open</small>
        </header>
        {data.decision_queue.map((item) => (
          <Link href={item.href} key={item.issue_id}>
            <span className={`projection-state is-${item.state}`}>{stateLabels[item.state]}</span>
            <strong>{item.title}</strong>
            <small>{item.pillar} · {item.artifact_type}</small>
            <b aria-hidden="true">→</b>
          </Link>
        ))}
      </section>

      <section className="collaboration-projection-list" aria-labelledby="grounding-owners-title">
        <header>
          <div>
            <span>Who is grounding what</span>
            <h2 id="grounding-owners-title">Reviewer round-trips</h2>
          </div>
          <small>{reviewSummary}</small>
        </header>
        {data.who_is_grounding_what.map((item) => (
          <Link href={item.href} key={`${item.issue_id}-${item.reviewer_name}`}>
            <span className="projection-state is-routed">{item.state}</span>
            <strong>{item.reviewer_name}</strong>
            <small>{item.issue_id}</small>
            <b aria-hidden="true">→</b>
          </Link>
        ))}
      </section>
    </section>
  );
}

export function CollaborationGroundingMap({ data }: { data: GroundingMapProjection }) {
  const total = data.nodes.length;
  const dense = total > 8;

  return (
    <section className="collaboration-projection grounding-map-projection" aria-labelledby="grounding-map-title">
      <header className="grounding-map-heading">
        <h1 id="grounding-map-title">Grounding map</h1>
        <p>what your plan rests on — grounded vs still OSLO-inferred</p>
      </header>
      <div className="grounding-map-progress">
        <strong>{data.counts.grounded} of {total} load-bearing details grounded</strong>
        <div aria-label={`${data.counts.grounded} of ${total} grounded`} role="img">
          {data.nodes.map((node) => (
            <span className={`is-${node.state}`} key={node.issue_id} />
          ))}
        </div>
      </div>

      <div
        className={`grounding-constellation ${dense ? "is-dense" : ""}`}
        data-node-density={dense ? "dense" : "standard"}
        aria-label="Grounding constellation"
      >
        <div className="grounding-plan-hub" aria-hidden="true">
          <span>Your plan</span>
          <i />
        </div>
        {data.nodes.map((node, index) => {
          const placement = groundingPlacement(index, total);
          return (
            <div className="grounding-orbit" key={node.issue_id} style={placement.style}>
              <span className={`grounding-connector is-${node.state}`} aria-hidden="true" />
              <Link
                aria-label={`${node.title}. ${stateLabels[node.state]}. Open issue`}
                className={`grounding-orbit-node is-${node.state} ${placement.labelPosition}`}
                href={node.href}
              >
                <i aria-hidden="true">
                  {node.state === "grounded" || node.state === "addressed" ? (
                    <Check size={11} weight="bold" />
                  ) : null}
                </i>
                <span>
                  <strong>{node.title}</strong>
                  <small>{node.detail || `${node.pillar} · ${node.artifact_type}`}</small>
                </span>
              </Link>
            </div>
          );
        })}
      </div>

      <div className="grounding-map-key" aria-label="Grounding states">
        {(Object.keys(groundingLegendLabels) as GroundingNodeState[])
          .filter((state) => data.counts[state] > 0)
          .map((state) => (
          <span className={`is-${state}`} key={state}>
            <i aria-hidden="true" />
            {groundingLegendLabels[state]} ({data.counts[state]})
          </span>
          ))}
      </div>
      <p className="grounding-map-explainer">
        Every load-bearing detail your plan rests on, in one view. Select a node to open its issue.
        The read is only as trustworthy as what it stands on — grounding a detail moves it from
        OSLO’s inference to your evidence.
      </p>
    </section>
  );
}
