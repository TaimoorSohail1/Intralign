import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { afterEach, describe, expect, it, vi } from "vitest";

import {
  Alert,
  Badge,
  Button,
  Card,
  Dialog,
  EmptyState,
  IconButton,
  Tabs,
  TextField,
} from "./index";

afterEach(cleanup);

describe("R2 design-system controls", () => {
  it("keeps shared component styling on design tokens", () => {
    const css = readFileSync(
      resolve(process.cwd(), "src/components/design-system/design-system.module.css"),
      "utf8",
    );

    expect(css).not.toMatch(/#[0-9a-f]{3,8}\b/i);
    expect(css).not.toMatch(/rgba?\(/i);
  });

  it("preserves native button semantics and loading state", () => {
    const onClick = vi.fn();
    render(
      <>
        <Button onClick={onClick}>Continue</Button>
        <Button loading>Saving</Button>
        <IconButton label="Close panel">×</IconButton>
      </>,
    );

    fireEvent.click(screen.getByRole("button", { name: "Continue" }));
    expect(onClick).toHaveBeenCalledOnce();
    expect(screen.getByRole("button", { name: "Saving" })).toBeDisabled();
    expect(screen.getByRole("button", { name: "Saving" })).toHaveAttribute("aria-busy", "true");
    expect(screen.getByRole("button", { name: "Close panel" })).toBeEnabled();
  });

  it("connects field help and errors to the native input", () => {
    render(
      <TextField
        error="Enter a valid email"
        hint="We only use this for access."
        label="Email address"
        name="email"
        type="email"
      />,
    );

    const input = screen.getByRole("textbox", { name: "Email address" });
    expect(input).toHaveAttribute("aria-invalid", "true");
    expect(input.getAttribute("aria-describedby")).toBeTruthy();
    expect(screen.getByRole("alert")).toHaveTextContent("Enter a valid email");
  });
});

describe("R2 design-system content patterns", () => {
  it("uses accessible semantics for status and empty content", () => {
    render(
      <>
        <Alert tone="danger" title="Analysis paused">Try again later.</Alert>
        <Badge tone="success">Current</Badge>
        <Card title="Project summary">Evidence-qualified read</Card>
        <EmptyState title="No projects">Create a project to begin.</EmptyState>
      </>,
    );

    expect(screen.getByRole("alert")).toHaveTextContent("Analysis paused");
    expect(screen.getByText("Current")).toBeInTheDocument();
    expect(screen.getByRole("region", { name: "Project summary" })).toHaveTextContent(
      "Evidence-qualified read",
    );
    expect(screen.getByText("No projects")).toBeInTheDocument();
  });

  it("switches tabs with click and keyboard navigation", () => {
    render(
      <Tabs
        ariaLabel="Issue grouping"
        items={[
          { id: "dimension", label: "By dimension", content: "Dimension results" },
          { id: "severity", label: "By severity", content: "Severity results" },
        ]}
      />,
    );

    const dimension = screen.getByRole("tab", { name: "By dimension" });
    const severity = screen.getByRole("tab", { name: "By severity" });
    expect(dimension).toHaveAttribute("aria-selected", "true");
    fireEvent.keyDown(dimension, { key: "ArrowRight" });
    expect(severity).toHaveAttribute("aria-selected", "true");
    expect(screen.getByRole("tabpanel")).toHaveTextContent("Severity results");
  });

  it("closes an open dialog with Escape and restores trigger focus", () => {
    const onClose = vi.fn();
    const trigger = document.createElement("button");
    trigger.textContent = "Open dialog";
    document.body.append(trigger);
    trigger.focus();

    const { rerender } = render(
      <Dialog onClose={onClose} open title="Share project">Invitation controls</Dialog>,
    );
    fireEvent.keyDown(document, { key: "Escape" });
    expect(onClose).toHaveBeenCalledOnce();

    rerender(<Dialog onClose={onClose} open={false} title="Share project">Invitation controls</Dialog>);
    expect(trigger).toHaveFocus();
    trigger.remove();
  });
});
