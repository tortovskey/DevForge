# Настраиваемое рабочее место

При проектировании изучались [открытый layout VS Code](https://github.com/microsoft/vscode/blob/main/src/vs/workbench/browser/layout.ts),
[раскладки VS Code](https://code.visualstudio.com/docs/configure/custom-layout),
[профили VS Code](https://code.visualstudio.com/docs/configure/profiles) и
[tool windows JetBrains](https://www.jetbrains.com/help/idea/tool-windows.html).
DevForge реализует собственный интерфейс и конфигурацию.

## Где менять поведение

| Файл | Ответственность |
|---|---|
| `frontend/src/ide/config.ts` | `THEMES`, `COMMANDS`, `FONTS`, `LAYOUT_PRESETS`, значения по умолчанию |
| `frontend/src/styles/workbench.css` | Компоненты и токены цветов `--ide-*` |
| `frontend/src/components/CodeEditor.tsx` | Перевод настроек в параметры и тему Monaco |
| `frontend/src/components/IDEResizer.tsx` | Перетаскивание и изменение размера клавиатурой |
| `frontend/src/services/store.tsx` | Последовательное сохранение и слияние изменений |
| `backend/app/ide_settings.py` | Типы, границы и проверка профилей |

Для новой команды добавьте запись в `COMMANDS`, обработчик в `DevForgeIDE.tsx`,
идентификатор и стандартное сочетание в серверную схему. Палитра и обработчик клавиш
используют один реестр. Клавиши определяются через `KeyboardEvent.code`, поэтому
сочетания не зависят от русской или английской раскладки. F1 зарезервирован для палитры.

## Профили

Текущая конфигурация хранится в `/api/settings`, коллекция — в `ideProfiles`.
У каждого профиля есть `id`, видимое `name` и `preferences`. Экспорт имеет оболочку:

```json
{
  "format": "devforge.ide-profile",
  "version": 1,
  "profile": {
    "id": "my-workbench",
    "name": "Моя мастерская",
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

Непереданные поля получают значения по умолчанию. Полная JSON Schema доступна
после входа через `GET /api/ide/profile-schema`; `POST /api/ide/validate-profile`
проверяет документ без записи. Сохранение выполняется отдельным PUT настроек.
Импорт интерфейса ограничен 64 КБ. Сервер запрещает неизвестные поля, произвольный
CSS, URL шрифтов, неизвестные команды и дублирующиеся сочетания.

Доступны шесть цветовых токенов: background, panel, editor, text, muted, border.
Значения — только `#RRGGBB`. Темы и профили не исполняют JavaScript.

## Развитие

Это точки расширения исходного кода. Загрузка сторонних VSIX/JAR и динамических
плагинов пока не реализована. Для новой настройки добавляйте серверную валидацию,
управление в редакторе настроек и проверку реального поведения Monaco/раскладки.
