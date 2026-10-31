# DevForge 1.0.0

A customizable coding workspace for Windows, built around the Monaco editor.
DevForge brings together local code execution, programming lessons, and a flexible
IDE workspace. The source code is available under the [MIT license](LICENSE).

**[Download installers](https://github.com/tortovskey/DevForge/releases/tag/v1.0.0)** ·
[Changelog](CHANGELOG.md) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) ·
[Test report](IDE/Source/TESTING.md)

![DevForge IDE workspace](IDE/Source/screenshots/workbench-dark.png)

## Choose your edition

| Edition | Purpose | Installer | Portable launch |
|---|---|---|---|
| IDE | Code editor, projects, and development tools | `IDE/Setup.exe` | `IDE/DevForgeIDE.exe` |
| Desktop | Programming lessons and the IDE in one desktop window | `Desktop/Setup.exe` | `Desktop/DevForge.exe` |

Version 1.0.0 ships as IDE and Desktop editions. The standalone Web edition has been
removed. Both editions use the blue forge icon, featuring a furnace and chimney.

DevForge requires Windows 10/11 x64 and Microsoft Edge WebView2. If WebView2 is
missing, Setup runs Microsoft's official bootstrapper; that step requires an
internet connection. The installers are not yet digitally signed.

## Make the workspace yours

- Six themes with custom accents and separate editor and panel colors.
- Code, Studio, and Focus layouts with movable and resizable panels.
- Configurable fonts, ligatures, line spacing, indentation, wrapping, guides, and cursor behavior.
- VS Code and JetBrains keyboard layouts with custom shortcuts and conflict detection.
- Up to 12 workspace profiles, JSON import/export, schema validation, and reset controls.
- A keyboard-driven command palette, split editing, project search, local snapshots, and a Python REPL.

Open IDE preferences using the sliders button above the editor or `Ctrl+,`.
Toggle focus mode with `Ctrl+Shift+F12`; the restore-panels button remains accessible.

![DevForge IDE preferences](IDE/Source/screenshots/workbench-preferences.png)

## Run from source

You need Git, Node.js 22.12+ (24 LTS recommended), Python 3.12, and WebView2.
Setup downloads dependencies from npm and PyPI, plus pinned runtime assets.
Additional Clang and SQLite downloads are verified with SHA-256. Packaged applications
serve these assets locally.

```powershell
git clone https://github.com/tortovskey/DevForge.git
cd DevForge/IDE/Source
./setup.bat
./start.bat                  # IDE
# & './Start Desktop.bat'    # Lessons and IDE
```

Application sources live in `IDE/Source/backend`, `frontend`, `content`, `assets`,
and `scripts`. Git excludes generated executables, databases, personal projects,
`.venv`, and `node_modules`.

IDE data is stored in `%LOCALAPPDATA%/DevForgeIDE/data`; Desktop data is stored in
`%LOCALAPPDATA%/DevForge/data`. Uninstalling the application preserves this data.

## Development and checks

After running Setup, use the following commands:

```powershell
cd IDE/Source
$env:DEVFORGE_DATA_DIR = "$PWD/build/test-data"
cd backend
../.venv/Scripts/python.exe -m pytest -q
cd ../frontend
npm run typecheck
npm run test:runner
npm run build
```

For interactive development, start the API from `IDE/Source/backend` in one terminal:

```powershell
$env:DEVFORGE_DATA_DIR = "$PWD/../build/dev-data"
../.venv/Scripts/python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

In another terminal, open `IDE/Source/frontend`, run `npm run assets`, then
`npm run dev -- --port 5174`. Run browser tests with:

```powershell
npm test -- ide.spec.ts security.spec.ts workbench.spec.ts
```

The browser is used to develop and test the interface. DevForge does not ship a
separate Web edition.

## Build the Windows applications

From `IDE/Source`, install the build dependencies into `.venv` with
`.venv/Scripts/python.exe -m pip install -r scripts/requirements-build.txt`.
Install Inno Setup, then run:

```powershell
./scripts/build-deliverables.ps1 -InnoCompiler "C:/Program Files (x86)/Inno Setup 7/ISCC.exe"
```

The build creates `build/distribution/IDE` and `build/distribution/Desktop`.
Each directory contains the application and its `Setup.exe` installer.

- Verify executable startup: `.venv/Scripts/python.exe scripts/verify_native.py`.
- Verify installation, upgrade, and removal in a test directory: `scripts/verify-installers.ps1`.

## Scope and runtime limitations

Code runs in browser Workers inside WebView2. Some languages use educational
interpreters with limited compatibility. The terminal supports DevForge commands,
and file snapshots are stored locally. These educational runtimes do not replace
a system shell, a production FastAPI server, or Git. The local API is intended
for use on `127.0.0.1`.

See [WORKBENCH.md](IDE/Source/WORKBENCH.md) for configuration and extension points.
Third-party components retain their [original licenses](IDE/Source/licenses/THIRD-PARTY.md).
