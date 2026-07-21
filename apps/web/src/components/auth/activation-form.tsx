"use client";

import { useState } from "react";

interface ActivationFormProps {
  email: string;
  token: string;
  workspaceName: string;
  action?: (formData: FormData) => void | Promise<void>;
}

export function ActivationForm({
  email,
  token,
  workspaceName,
  action,
}: ActivationFormProps) {
  const [passwordError, setPasswordError] = useState("");

  return (
    <form
      action={action}
      className="activation-card"
      onSubmit={(event) => {
        const formData = new FormData(event.currentTarget);
        if (formData.get("password") !== formData.get("confirm_password")) {
          event.preventDefault();
          setPasswordError("Passwords do not match");
        } else {
          setPasswordError("");
        }
      }}
    >
      <input name="token" type="hidden" value={token} />
      <h1>Activate your account</h1>
      <p className="activation-subtitle">
        Set your credentials to join {workspaceName} and finish activation.
      </p>

      <div className="field">
        <label htmlFor="invited-email">Email (from your invite)</label>
        <input
          aria-readonly="true"
          id="invited-email"
          name="email"
          readOnly
          type="email"
          value={email}
        />
      </div>

      <div className="field">
        <label htmlFor="display-name">Display name</label>
        <input
          autoComplete="name"
          id="display-name"
          minLength={1}
          name="display_name"
          required
          type="text"
        />
      </div>

      <div className="field">
        <label htmlFor="new-password">Choose a password</label>
        <input
          autoComplete="new-password"
          id="new-password"
          minLength={12}
          name="password"
          placeholder="••••••••••••"
          required
          type="password"
        />
      </div>

      <div className="field">
        <label htmlFor="confirm-password">Confirm password</label>
        <input
          autoComplete="new-password"
          id="confirm-password"
          minLength={12}
          name="confirm_password"
          required
          type="password"
        />
      </div>
      {passwordError ? <p className="form-error" role="alert">{passwordError}</p> : null}

      <label className="stay-signed-in">
        <input defaultChecked name="stay_signed_in" type="checkbox" value="true" />
        <span>Stay signed in on this device</span>
      </label>

      <button className="button button-primary button-full" type="submit">
        Create account &amp; continue <span aria-hidden="true">→</span>
      </button>
    </form>
  );
}
