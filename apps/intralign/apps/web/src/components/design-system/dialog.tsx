"use client";

import { X } from "@phosphor-icons/react";
import {
  useEffect,
  useId,
  useRef,
  type MouseEvent,
  type PropsWithChildren,
  type ReactNode,
} from "react";

import styles from "./design-system.module.css";

export interface DialogProps extends PropsWithChildren {
  actions?: ReactNode;
  description?: string;
  onClose: () => void;
  open: boolean;
  title: string;
}

export function Dialog({ actions, children, description, onClose, open, title }: DialogProps) {
  const titleId = useId();
  const descriptionId = useId();
  const closeRef = useRef<HTMLButtonElement>(null);
  const returnFocusRef = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (!open) return;
    returnFocusRef.current = document.activeElement as HTMLElement | null;
    closeRef.current?.focus();

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        onClose();
      }
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.removeEventListener("keydown", closeOnEscape);
      returnFocusRef.current?.focus();
    };
  }, [onClose, open]);

  if (!open) return null;

  const closeFromBackdrop = (event: MouseEvent<HTMLDivElement>) => {
    if (event.target === event.currentTarget) onClose();
  };

  return (
    <div className={styles.dialogBackdrop} onMouseDown={closeFromBackdrop}>
      <section
        aria-describedby={description ? descriptionId : undefined}
        aria-labelledby={titleId}
        aria-modal="true"
        className={styles.dialog}
        role="dialog"
      >
        <header className={styles.dialogHeader}>
          <div>
            <h2 id={titleId}>{title}</h2>
            {description ? <p id={descriptionId}>{description}</p> : null}
          </div>
          <button
            aria-label="Close dialog"
            className={`${styles.button} ${styles.buttonGhost} ${styles.buttonSmall} ${styles.iconButton}`}
            onClick={onClose}
            ref={closeRef}
            type="button"
          >
            <X aria-hidden="true" size={18} />
          </button>
        </header>
        <div className={styles.dialogBody}>{children}</div>
        {actions ? <footer className={styles.dialogFooter}>{actions}</footer> : null}
      </section>
    </div>
  );
}
