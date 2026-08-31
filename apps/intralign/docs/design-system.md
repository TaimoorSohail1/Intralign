# R2 design system

The shared design system is the UI contract for Release 2. It preserves the approved R2 prototype language while reducing duplicated styling and interaction code.

## Foundations

- Tokens: `apps/web/src/styles/tokens.css`
- Components: `apps/web/src/components/design-system/`
- Global compatibility layer: `apps/web/src/app/globals.css`

Tokens cover semantic colour, typography, spacing, radii, elevation, control sizing, motion, layout widths, focus, and z-index. Dark mode is the R2 default; light-mode values remain available through `data-theme="light"`.

## Shared components

- Actions: `Button`, `IconButton`
- Forms: `TextField`, `TextAreaField`, `SelectField`, `CheckboxField`
- Content: `Badge`, `Card`, `Alert`, `EmptyState`
- Layout: `Stack`, `Inline`, `VisuallyHidden`
- Interaction: `Dialog`, `Tabs`

Components keep native HTML semantics, keyboard behaviour, focus handling, labels, descriptions, errors, loading states, and disabled states. Shared component CSS must use semantic tokens rather than raw colour values.

## Adoption rule

New R2 UI must use the shared components and tokens. Existing slice CSS can migrate incrementally because the global legacy variables now resolve to the same semantic token contract. A migration must preserve approved R2 hierarchy, wording, state, and behaviour; the design system is not permission to restyle the product.

## Verification

Run:

```powershell
pnpm --filter @oslo/web exec vitest run src/components/design-system/design-system.test.tsx --pool=threads --maxWorkers=1
pnpm --filter @oslo/web exec vitest run --pool=threads --maxWorkers=1
pnpm --filter @oslo/web lint
pnpm --filter @oslo/web build
```

The focused suite checks component semantics, field accessibility, keyboard tabs, dialog focus restoration, and the no-raw-colour rule for shared component styles.
