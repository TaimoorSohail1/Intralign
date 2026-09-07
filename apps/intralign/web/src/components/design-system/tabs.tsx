"use client";

import { useId, useRef, useState, type KeyboardEvent, type ReactNode } from "react";

import styles from "./design-system.module.css";

export interface TabItem {
  content: ReactNode;
  disabled?: boolean;
  id: string;
  label: ReactNode;
}

export interface TabsProps {
  ariaLabel: string;
  defaultId?: string;
  items: TabItem[];
}

export function Tabs({ ariaLabel, defaultId, items }: TabsProps) {
  const groupId = useId().replaceAll(":", "");
  const enabledItems = items.filter((item) => !item.disabled);
  const initialId = enabledItems.some((item) => item.id === defaultId)
    ? defaultId
    : enabledItems[0]?.id;
  const [selectedId, setSelectedId] = useState(initialId);
  const refs = useRef(new Map<string, HTMLButtonElement>());
  const selected = items.find((item) => item.id === selectedId) ?? enabledItems[0];

  function selectAndFocus(id: string) {
    setSelectedId(id);
    requestAnimationFrame(() => refs.current.get(id)?.focus());
  }

  function handleKeyDown(event: KeyboardEvent<HTMLButtonElement>, currentId: string) {
    const currentIndex = enabledItems.findIndex((item) => item.id === currentId);
    if (currentIndex < 0 || enabledItems.length < 2) return;

    let nextIndex: number | undefined;
    if (event.key === "ArrowRight") nextIndex = (currentIndex + 1) % enabledItems.length;
    if (event.key === "ArrowLeft") nextIndex = (currentIndex - 1 + enabledItems.length) % enabledItems.length;
    if (event.key === "Home") nextIndex = 0;
    if (event.key === "End") nextIndex = enabledItems.length - 1;
    if (nextIndex === undefined) return;

    event.preventDefault();
    selectAndFocus(enabledItems[nextIndex].id);
  }

  if (!selected) return null;

  return (
    <div className={styles.tabs}>
      <div aria-label={ariaLabel} className={styles.tabList} role="tablist">
        {items.map((item) => {
          const active = item.id === selected.id;
          return (
            <button
              aria-controls={`${groupId}-panel-${item.id}`}
              aria-selected={active}
              className={styles.tab}
              disabled={item.disabled}
              id={`${groupId}-tab-${item.id}`}
              key={item.id}
              onClick={() => setSelectedId(item.id)}
              onKeyDown={(event) => handleKeyDown(event, item.id)}
              ref={(node) => {
                if (node) refs.current.set(item.id, node);
                else refs.current.delete(item.id);
              }}
              role="tab"
              tabIndex={active ? 0 : -1}
              type="button"
            >
              {item.label}
            </button>
          );
        })}
      </div>
      <div
        aria-labelledby={`${groupId}-tab-${selected.id}`}
        className={styles.tabPanel}
        id={`${groupId}-panel-${selected.id}`}
        role="tabpanel"
        tabIndex={0}
      >
        {selected.content}
      </div>
    </div>
  );
}
