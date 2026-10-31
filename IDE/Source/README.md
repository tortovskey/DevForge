# DevForge 1.0.0 source code

See the [project README](../../README.md) for setup, development, testing, and build
instructions. DevForge is licensed under [MIT](../../LICENSE) and ships in two
editions: IDE and Desktop.

- `frontend/src/ide/config.ts`: themes, commands, and layout registries.
- `frontend/src/components/IDECustomization.tsx`: the preferences editor.
- `backend/app/ide_settings.py`: strict profile validation.
- `frontend/tests/workbench.spec.ts` and `backend/tests/test_ide_settings.py`: preference checks.
- `scripts/build-deliverables.ps1`: executable and Setup builds for both editions.
- [WORKBENCH.md](WORKBENCH.md): extending the interface and configuration format.
- [TESTING.md](TESTING.md): verification results and their limits.

Local `data`, `build`, `release`, `.venv`, and `node_modules` directories are excluded
from Git. They may contain personal data, logs, or archived application builds.
