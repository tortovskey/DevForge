# DevForge 1.0.1 verification

## 1.0.1 release checks — 2026-11-02

- Backend: 75 passed. Runtime and backup-format checks: 9 passed.
- Production Playwright suites (IDE, workbench, security, production): 26 passed.
- Windows IDE and Desktop binaries and installers: built with version 1.0.1.
- Both editions: installation, reinstall/upgrade, native startup, and removal verified in isolated workspace folders.
- Desktop startup timed out during concurrent checks; an isolated retry passed and the Python worker printed `42`.

## IDE refresh — 2026-10-31

- TypeScript and production frontend build: passed.
- Playwright IDE and workbench suites: 19 passed, including Assembly/Lua project creation and execution, run-file selection, panel restoration, and smaller windows.
- Assembly and Lua creation/run checks against the production bundle: 2 passed.
- Runtime and backup-format tests: 9 passed.
- Rebuilt Windows IDE and installer; native IDE startup verification passed.
- Visually checked the dark workbench, preferences, light search panel, 760px window, and Assembly output/registers. Updated screenshots are in `screenshots/`.

Existing projects are preserved. An Assembly project previously created with `query.sql` is not rewritten automatically; source containing Assembly must be saved with an `.asm` extension.

## Original 1.0.0 release verification

Date: 2026-10-31. Environment: Windows x64, Python 3.12, Node.js, Chromium/Edge,
and WebView2. Test databases and accounts are isolated from personal data.

| Check | Result |
|---|---|
| Backend: `pytest -q` | 75 passed |
| Code execution and sync format validation | 9 passed |
| Playwright: IDE, production, security, workbench | 22 scenarios verified |
| TypeScript and production build | Passed |
| Clang/SQLite downloads into an empty directory | Passed; SHA-256 hashes matched |
| Curriculum integrity | 377 lessons, 0 structural issues |
| npm audit | 0 known vulnerabilities |
| Full Python environment audit | 63 packages, 0 known vulnerabilities after updating pip |
| IDE and Desktop installers | Installation, reinstall/upgrade, and removal passed |
| Installed IDE and Desktop startup | Passed; Monaco, icon, isolation; Python output was 42 |
| Portable IDE and Desktop startup from an unrelated directory | Both passed |

The full browser run passed 21 scenarios. One autocomplete scenario stopped during
browser page creation, before the application code ran. An isolated rerun passed
in 7 seconds. No product changes were made to work around that infrastructure failure.

## Coverage

- Editor startup without JavaScript errors, revision saves, and draft recovery.
- Editing during a save and restoring edits after a reload.
- Python input(), REPL, HTML sandboxing, and local runtimes.
- Blocking user Worker access to the account API and external network.
- Valid backup import, malformed file handling, and automatic backup creation.
- Monaco themes, actual font/indentation options, and persistent preferences.
- Panel docking, resizing, and restoration from focus mode.
- JSON profiles, shortcut conflicts, JetBrains keymaps, and keyboard palette navigation.
- Closing a tab preserves its file; failed preference saves can be retried.
- Usable controls at window widths of 760 and 1000 pixels.

The 1.0 update fixed backup version validation in the interface. It accepts 1.0.x
and older 0.4.x/0.5.x files. Server and client compatibility checks were added.
Closing a tab no longer invokes file deletion.

## Limits of verification

Automated checks cover the scenarios above and do not prove that all bugs are
absent. The installers are not digitally signed. Vite reports a Monaco chunk-size
warning, but the build succeeds. Pytest reports a deprecated httpx adapter in
Starlette TestClient; this does not change application HTTP requests. CI checks
the backend and frontend build on Linux. Native windows and installers were
verified on Windows.

Detailed local logs are stored in the ignored `build/release-*` paths. Test
databases, personal projects, and session logs are excluded from the repository.

CI creates a complete production frontend build before running runtime and backend
checks. These tests use the actual built Lua bundle, SVG icon, assets/runtimes/workers
directories, and index.html.
