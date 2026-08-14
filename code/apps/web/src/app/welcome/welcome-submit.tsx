"use client";

import { useFormStatus } from "react-dom";

export function WelcomeSubmitButton() {
  const { pending } = useFormStatus();
  return (
    <button
      aria-label={pending ? "Starting your outcome" : undefined}
      className="button button-primary"
      disabled={pending}
      type="submit"
    >
      {pending ? "Starting your outcome…" : "Start your first outcome"}{" "}
      <span aria-hidden="true">→</span>
    </button>
  );
}
