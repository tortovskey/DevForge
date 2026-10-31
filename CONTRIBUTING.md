# Участие в DevForge

DevForge распространяется под MIT. Рабочие исходники находятся в `IDE/Source/`;
папки `IDE` и `Desktop` также служат местом для локальных сборок, которые Git игнорирует.

1. Создайте fork и ветку для одного изменения.
2. Установите зависимости по README и запустите проверки ниже.
3. Опишите проблему, изменение и проверку в pull request. Для интерфейса приложите снимок.

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

Для браузерных тестов запустите API и Vite в отдельных терминалах по README,
затем `npm test -- ide.spec.ts security.spec.ts workbench.spec.ts`.
Тесты используют отдельные учётные записи и временные базы; личные данные не нужны.

Темы, шрифты, команды и раскладки описаны в `frontend/src/ide/config.ts`.
Добавляя настройку, обновите типы, `backend/app/ide_settings.py`, интерфейс и проверки.
Формат профиля версионируется отдельно от версии приложения.

Не включайте в PR базы данных, токены, `.env`, сборки, `node_modules` или чужие проекты.
У новых внешних компонентов должны быть совместимая лицензия и запись в `licenses/`.
