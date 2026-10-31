# Contributing to DevForge

DevForge is licensed under MIT. Development sources are in `IDE/Source/`.
The top-level `IDE` and `Desktop` directories also hold local application builds,
which Git ignores.

1. Fork the repository and create a branch for one focused change.
2. Install the dependencies using the README and run the checks below.
3. Describe the problem, the resulting behavior, and your validation in the pull request.
   Include a screenshot for interface changes.

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

For browser tests, start the API and Vite in separate terminals as described in the
README, then run `npm test -- ide.spec.ts security.spec.ts workbench.spec.ts`.
Tests use separate accounts and temporary databases; personal data is not needed.

Themes, fonts, commands, and layouts are defined in `frontend/src/ide/config.ts`.
When adding a preference, update its types, `backend/app/ide_settings.py`, the
preferences interface, and relevant checks. The profile format is versioned
independently of the application.

Keep databases, tokens, `.env`, generated builds, `node_modules`, and other people's
projects out of pull requests. New third-party components need a compatible license
and a notice in `licenses/`.
