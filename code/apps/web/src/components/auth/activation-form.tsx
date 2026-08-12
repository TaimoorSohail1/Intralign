"use client";

import Link from "next/link";

interface ActivationFormProps {
  email: string;
  token: string;
  workspaceName: string;
  action?: (formData: FormData) => void | Promise<void>;
}

const roleOptions = [
  ["run", "I run the plan", "Delivery / project PM"],
  ["own", "I own the outcome", "Business / functional owner"],
  ["both", "I own it and run it", "Outcome owner + delivery lead"],
  ["other", "Something else", "Other / not sure"],
] as const;

function displayNameFromEmail(email: string) {
  return email
    .split("@", 1)[0]
    .split(/[._-]+/)
    .filter(Boolean)
    .map((part) => `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
    .join(" ");
}

export function ActivationForm({ email, token, action }: ActivationFormProps) {
  return (
    <form action={action} className="activation-card">
      <input name="token" type="hidden" value={token} />
      <h1>Activate your account</h1>
      <p className="activation-subtitle">Set your credentials to finish activation.</p>

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
          defaultValue={displayNameFromEmail(email)}
          id="display-name"
          minLength={1}
          name="display_name"
          required
          type="text"
        />
      </div>

      <fieldset className="activation-role-fieldset">
        <legend>
          How do you work with this plan?
          <span>Shapes what OSLO puts first — never the read itself</span>
        </legend>
        <div className="activation-role-grid">
          {roleOptions.map(([value, title, detail], index) => (
            <label className="activation-role-card" key={value}>
              <input defaultChecked={index === 0} name="role_context" type="radio" value={value} />
              <span className="activation-role-title">{title}</span>
              <span className="activation-role-detail">{detail}</span>
            </label>
          ))}
        </div>
      </fieldset>

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

      <label className="stay-signed-in">
        <input defaultChecked name="stay_signed_in" type="checkbox" value="true" />
        <span>Stay signed in on this device</span>
      </label>

      <button className="button button-primary button-full" type="submit">
        Create account &amp; continue <span aria-hidden="true">→</span>
      </button>
      <Link className="activation-back-link" href={`/activate?token=${encodeURIComponent(token)}`}>
        ← Back to the invitation
      </Link>
    </form>
  );
}
