# Changelog

## 1.0.1 — 2026-11-02

- Reworked the IDE into a single full-window workbench with a compact toolbar, aligned file explorer, file breadcrumbs, and consistent theme-aware controls.
- Added visible controls to restore panels and connected the run-file selector to the active editor.
- Fixed Assembly and Lua project creation: each language now gets its own source file and runnable template instead of SQL. Project templates are checked against all supported languages by TypeScript.
- Recognized Assembly `.inc` files and C++ `.cxx` files consistently when selecting a runtime.

## 1.0.0 — 2026-10-31

- Released the source code under MIT, with IDE and Desktop editions for Windows.
- Removed the standalone Web edition from releases and build commands.
- Added six themes with shared Monaco and workbench palettes, custom accents, and color overrides.
- Added Code, Studio, and Focus layouts with movable and resizable panels.
- Expanded font, indentation, wrapping, cursor, and completion settings.
- Added VS Code and JetBrains keymaps with custom bindings and conflict detection.
- Added up to 12 profiles, JSON import/export, and a downloadable JSON Schema.
- Added keyboard navigation to the command palette; closing a tab now preserves its file.
- Added verified runtime downloads to support builds from a clean clone.
- Added installers with the MIT license, version information, and the blue forge icon.
