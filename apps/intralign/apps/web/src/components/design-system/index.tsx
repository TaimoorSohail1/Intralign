import {
  forwardRef,
  useId,
  type ButtonHTMLAttributes,
  type CSSProperties,
  type HTMLAttributes,
  type InputHTMLAttributes,
  type PropsWithChildren,
  type ReactNode,
  type SelectHTMLAttributes,
  type TextareaHTMLAttributes,
} from "react";

import styles from "./design-system.module.css";

function classes(...values: Array<string | false | null | undefined>) {
  return values.filter(Boolean).join(" ");
}

type ButtonVariant = "primary" | "secondary" | "ghost" | "danger";
type ButtonSize = "small" | "medium" | "large";

const buttonVariants: Record<ButtonVariant, string> = {
  primary: styles.buttonPrimary,
  secondary: styles.buttonSecondary,
  ghost: styles.buttonGhost,
  danger: styles.buttonDanger,
};

const buttonSizes: Record<ButtonSize, string | undefined> = {
  small: styles.buttonSmall,
  medium: undefined,
  large: styles.buttonLarge,
};

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  fullWidth?: boolean;
  loading?: boolean;
  size?: ButtonSize;
  variant?: ButtonVariant;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(function Button(
  {
    children,
    className,
    disabled,
    fullWidth = false,
    loading = false,
    size = "medium",
    type = "button",
    variant = "primary",
    ...props
  },
  ref,
) {
  return (
    <button
      {...props}
      aria-busy={loading || undefined}
      className={classes(
        styles.button,
        buttonVariants[variant],
        buttonSizes[size],
        fullWidth && styles.buttonFull,
        className,
      )}
      disabled={disabled || loading}
      ref={ref}
      type={type}
    >
      {loading ? <span aria-hidden="true" className={styles.spinner} /> : null}
      {children}
    </button>
  );
});

export interface IconButtonProps extends Omit<ButtonProps, "aria-label"> {
  label: string;
}

export const IconButton = forwardRef<HTMLButtonElement, IconButtonProps>(function IconButton(
  { className, label, variant = "ghost", ...props },
  ref,
) {
  return (
    <Button
      {...props}
      aria-label={label}
      className={classes(styles.iconButton, className)}
      ref={ref}
      variant={variant}
    />
  );
});

interface FieldCopy {
  error?: string;
  hint?: string;
  label: string;
}

function FieldFrame({
  children,
  error,
  hint,
  id,
  label,
  required,
}: PropsWithChildren<FieldCopy & { id: string; required?: boolean }>) {
  return (
    <div className={styles.field}>
      <label className={classes(styles.fieldLabel, required && styles.fieldLabelRequired)} htmlFor={id}>
        {label}
      </label>
      {children}
      {hint ? <p className={styles.fieldHint} id={`${id}-hint`}>{hint}</p> : null}
      {error ? <p className={styles.fieldError} id={`${id}-error`} role="alert">{error}</p> : null}
    </div>
  );
}

function describedBy(id: string, hint?: string, error?: string, supplied?: string) {
  return [supplied, hint ? `${id}-hint` : null, error ? `${id}-error` : null]
    .filter(Boolean)
    .join(" ") || undefined;
}

export interface TextFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "size">, FieldCopy {}

export const TextField = forwardRef<HTMLInputElement, TextFieldProps>(function TextField(
  { "aria-describedby": ariaDescribedBy, className, error, hint, id: suppliedId, label, required, ...props },
  ref,
) {
  const generatedId = useId();
  const id = suppliedId ?? generatedId;
  return (
    <FieldFrame error={error} hint={hint} id={id} label={label} required={required}>
      <input
        {...props}
        aria-describedby={describedBy(id, hint, error, ariaDescribedBy)}
        aria-invalid={error ? true : undefined}
        className={classes(styles.fieldControl, className)}
        id={id}
        ref={ref}
        required={required}
      />
    </FieldFrame>
  );
});

export interface TextAreaFieldProps extends TextareaHTMLAttributes<HTMLTextAreaElement>, FieldCopy {}

export const TextAreaField = forwardRef<HTMLTextAreaElement, TextAreaFieldProps>(function TextAreaField(
  { "aria-describedby": ariaDescribedBy, className, error, hint, id: suppliedId, label, required, ...props },
  ref,
) {
  const generatedId = useId();
  const id = suppliedId ?? generatedId;
  return (
    <FieldFrame error={error} hint={hint} id={id} label={label} required={required}>
      <textarea
        {...props}
        aria-describedby={describedBy(id, hint, error, ariaDescribedBy)}
        aria-invalid={error ? true : undefined}
        className={classes(styles.fieldControl, className)}
        id={id}
        ref={ref}
        required={required}
      />
    </FieldFrame>
  );
});

export interface SelectFieldProps extends SelectHTMLAttributes<HTMLSelectElement>, FieldCopy {}

export const SelectField = forwardRef<HTMLSelectElement, SelectFieldProps>(function SelectField(
  { "aria-describedby": ariaDescribedBy, children, className, error, hint, id: suppliedId, label, required, ...props },
  ref,
) {
  const generatedId = useId();
  const id = suppliedId ?? generatedId;
  return (
    <FieldFrame error={error} hint={hint} id={id} label={label} required={required}>
      <select
        {...props}
        aria-describedby={describedBy(id, hint, error, ariaDescribedBy)}
        aria-invalid={error ? true : undefined}
        className={classes(styles.fieldControl, className)}
        id={id}
        ref={ref}
        required={required}
      >
        {children}
      </select>
    </FieldFrame>
  );
});

export interface CheckboxFieldProps extends Omit<InputHTMLAttributes<HTMLInputElement>, "type"> {
  hint?: string;
  label: string;
}

export const CheckboxField = forwardRef<HTMLInputElement, CheckboxFieldProps>(function CheckboxField(
  { className, hint, id: suppliedId, label, ...props },
  ref,
) {
  const generatedId = useId();
  const id = suppliedId ?? generatedId;
  return (
    <label className={classes(styles.checkboxField, className)} htmlFor={id}>
      <input {...props} id={id} ref={ref} type="checkbox" />
      <span className={styles.checkboxCopy}>
        <strong>{label}</strong>
        {hint ? <small>{hint}</small> : null}
      </span>
    </label>
  );
});

type BadgeTone = "neutral" | "accent" | "success" | "warning" | "danger" | "info";
const badgeTones: Record<BadgeTone, string | undefined> = {
  neutral: undefined,
  accent: styles.badgeAccent,
  success: styles.badgeSuccess,
  warning: styles.badgeWarning,
  danger: styles.badgeDanger,
  info: styles.badgeInfo,
};

export function Badge({ children, className, tone = "neutral", ...props }: HTMLAttributes<HTMLSpanElement> & { tone?: BadgeTone }) {
  return <span {...props} className={classes(styles.badge, badgeTones[tone], className)}>{children}</span>;
}

export interface CardProps extends HTMLAttributes<HTMLElement> {
  description?: string;
  raised?: boolean;
  title?: string;
}

export function Card({ children, className, description, raised = false, title, ...props }: CardProps) {
  const titleId = useId();
  return (
    <section
      {...props}
      aria-labelledby={title ? titleId : undefined}
      className={classes(styles.card, raised && styles.cardRaised, className)}
    >
      {title || description ? (
        <header className={styles.cardHeader}>
          {title ? <h2 className={styles.cardTitle} id={titleId}>{title}</h2> : null}
          {description ? <p className={styles.cardDescription}>{description}</p> : null}
        </header>
      ) : null}
      {children}
    </section>
  );
}

type AlertTone = "info" | "success" | "warning" | "danger";
const alertTones: Record<AlertTone, string> = {
  info: styles.alertInfo,
  success: styles.alertSuccess,
  warning: styles.alertWarning,
  danger: styles.alertDanger,
};

export function Alert({ children, className, title, tone = "info", ...props }: HTMLAttributes<HTMLDivElement> & { title: string; tone?: AlertTone }) {
  return (
    <div
      {...props}
      className={classes(styles.alert, alertTones[tone], className)}
      role={tone === "danger" ? "alert" : "status"}
    >
      <span aria-hidden="true" className={styles.alertMark} />
      <div className={styles.alertBody}><strong>{title}</strong><div>{children}</div></div>
    </div>
  );
}

export function EmptyState({ actions, children, className, title, ...props }: HTMLAttributes<HTMLDivElement> & { actions?: ReactNode; title: string }) {
  return (
    <div {...props} className={classes(styles.emptyState, className)}>
      <strong>{title}</strong>
      <p>{children}</p>
      {actions ? <div className={styles.emptyStateActions}>{actions}</div> : null}
    </div>
  );
}

type Gap = "1" | "2" | "3" | "4" | "5" | "6" | "8";
type GapStyle = CSSProperties & { "--stack-gap"?: string; "--inline-gap"?: string };

export function Stack({ children, className, gap = "4", style, ...props }: HTMLAttributes<HTMLDivElement> & { gap?: Gap }) {
  return <div {...props} className={classes(styles.stack, className)} style={{ ...style, "--stack-gap": `var(--space-${gap})` } as GapStyle}>{children}</div>;
}

export function Inline({ children, className, gap = "3", style, ...props }: HTMLAttributes<HTMLDivElement> & { gap?: Gap }) {
  return <div {...props} className={classes(styles.inline, className)} style={{ ...style, "--inline-gap": `var(--space-${gap})` } as GapStyle}>{children}</div>;
}

export function VisuallyHidden({ children }: PropsWithChildren) {
  return <span className={styles.visuallyHidden}>{children}</span>;
}

export { Dialog, type DialogProps } from "./dialog";
export { Tabs, type TabItem, type TabsProps } from "./tabs";
