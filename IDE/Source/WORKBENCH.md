# Customizable workbench

The workbench design was informed by the [open VS Code layout implementation](https://github.com/microsoft/vscode/blob/main/src/vs/workbench/browser/layout.ts),
[VS Code layout options](https://code.visualstudio.com/docs/configure/custom-layout),
[VS Code profiles](https://code.visualstudio.com/docs/configure/profiles), and
[JetBrains tool windows](https://www.jetbrains.com/help/idea/tool-windows.html).
DevForge implements its own interface and configuration.

## Where behavior is defined

| File | Responsibility |
|---|---|
| `frontend/src/ide/config.ts` | `THEMES`, `COMMANDS`, `FONTS`, `LAYOUT_PRESETS`, and defaults |
| `frontend/src/styles/workbench.css` | Components and `--ide-*` color tokens |
| `frontend/src/components/CodeEditor.tsx` | Mapping preferences to Monaco options and themes |
| `frontend/src/components/IDEResizer.tsx` | Pointer and keyboard resizing |
| `frontend/src/services/store.tsx` | Sequential settings saves and patch merging |
| `backend/app/ide_settings.py` | Profile types, bounds, and validation |

To add a command, register it in `COMMANDS`, add its handler in `DevForgeIDE.tsx`,
and add its identifier and default binding to the server schema. The command
palette and keyboard handler share one registry. Keys are identified through
`KeyboardEvent.code`, so shortcuts work independently of the Russian or English
keyboard layout. F1 is reserved for the command palette.

## Profiles

The current configuration is stored through `/api/settings`; saved profiles are
in `ideProfiles`. Each profile has an `id`, a display `name`, and `preferences`.
An exported document uses this envelope:

```json
{
  "format": "devforge.ide-profile",
  "version": 1,
  "profile": {
    "id": "my-workbench",
    "name": "My workbench",
    "preferences": {
      "theme": "dark",
      "fontSize": 16,
      "minimap": true,
      "inlineCompletion": true,
      "ide": {"theme": "nord", "tabSize": 2, "wordWrap": "on"}
    }
  }
}
```

Omitted fields receive their default values. After authentication, retrieve the
full JSON Schema from `GET /api/ide/profile-schema`. Use
`POST /api/ide/validate-profile` to validate a document without writing settings.
Saving requires a separate settings PUT request.

The interface limits profile imports to 64 KB. The server rejects unknown fields,
arbitrary CSS, font URLs, unknown commands, and duplicate shortcut assignments.

Six color tokens are available: background, panel, editor, text, muted, and border.
Values must use `#RRGGBB`. Themes and profiles do not execute JavaScript.

## Extending the workbench

These are source-level extension points. Loading third-party VSIX/JAR packages or
dynamic plugins is not implemented. For a new preference, add server validation,
a control in the preferences editor, and checks of the actual Monaco or layout
behavior.
