# Исходники DevForge 1.0.0

Инструкции по запуску, проверке и сборке: [README проекта](../../README.md).
Лицензия: [MIT](../../LICENSE). Две поставки: IDE и Desktop.

- `frontend/src/ide/config.ts`: темы, команды и раскладки.
- `frontend/src/components/IDECustomization.tsx`: редактор настроек.
- `backend/app/ide_settings.py`: строгая схема профилей.
- `frontend/tests/workbench.spec.ts`, `backend/tests/test_ide_settings.py`: проверки настроек.
- `scripts/build-deliverables.ps1`: EXE и Setup для обеих версий.
- `WORKBENCH.md`: расширение интерфейса и формата конфигурации.

Локальные папки `data`, `build`, `release`, `.venv`, `node_modules` исключены из Git.
Они могут содержать личные данные, журналы и архивы предыдущих сборок.
