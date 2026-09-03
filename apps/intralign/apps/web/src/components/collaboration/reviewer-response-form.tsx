"use client";

import { CheckCircle, XCircle } from "@phosphor-icons/react";
import { FormEvent, useState } from "react";

const responses = [
  { value: "approve", label: "Confirm", Icon: CheckCircle },
  { value: "reject", label: "Reject", Icon: XCircle },
] as const;

export function ReviewerResponseForm({ token }: { token: string }) {
  const [kind, setKind] = useState<(typeof responses)[number]["value"]>("approve");
  const [body, setBody] = useState("");
  const [pending, setPending] = useState(false);
  const [result, setResult] = useState<"success" | "error" | null>(null);
  const [message, setMessage] = useState("");

  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setPending(true);
    setResult(null);
    try {
      const response = await fetch(`/api/public/review/${encodeURIComponent(token)}`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ kind, body: body.trim() }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(payload.message ?? "Your response could not be submitted.");
      setResult("success");
      setMessage(
        "Your response is recorded as attributed evidence and the project read is updating.",
      );
    } catch (caught) {
      setResult("error");
      setMessage(caught instanceof Error ? caught.message : "Your response could not be submitted.");
    } finally {
      setPending(false);
    }
  };

  if (result === "success") {
    return (
      <section className="review-response-success" aria-live="polite">
        <CheckCircle size={28} weight="fill" />
        <div>
          <h2>Thank you for the review</h2>
          <p>{message}</p>
          <small>No account or workspace seat was created.</small>
        </div>
      </section>
    );
  }

  return (
    <form className="review-response-form" onSubmit={submit}>
      <fieldset>
        <legend>Your response</legend>
        <div className="review-response-options">
          {responses.map(({ value, label, Icon }) => (
            <label className={kind === value ? "is-selected" : ""} key={value}>
              <input
                checked={kind === value}
                name="review-kind"
                onChange={() => setKind(value)}
                type="radio"
                value={value}
              />
              <Icon aria-hidden="true" size={18} />
              <span>{label}</span>
            </label>
          ))}
        </div>
      </fieldset>
      <label className="review-response-note">
        <span>Reviewer note</span>
        <textarea
          disabled={pending}
          maxLength={5_000}
          onChange={(event) => setBody(event.target.value)}
          placeholder="Cite the evidence behind your confirmation or rejection."
          required
          value={body}
        />
      </label>
      <p className="review-response-policy">
        Your response becomes a traceable reviewer attestation. Only the governed
        reanalysis can change or close the issue.
      </p>
      <button disabled={pending || !body.trim()} type="submit">
        {pending ? "Submitting…" : "Submit review"}
      </button>
      {result === "error" ? <p className="review-response-error" role="alert">{message}</p> : null}
    </form>
  );
}
