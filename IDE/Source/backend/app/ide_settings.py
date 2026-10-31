"""Versioned, data-only workbench configuration. No CSS or executable plugins."""
import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

COMMANDS = ('run', 'save', 'format', 'split', 'palette', 'files', 'search',
            'terminal', 'sidebar', 'panel', 'settings', 'zen', 'previousTab', 'nextTab')
CODE_KEYS = dict(zip(COMMANDS, ('Ctrl+Enter', 'Ctrl+S', 'Alt+Shift+F', 'Ctrl+Backslash',
    'Ctrl+Shift+P', 'Ctrl+P', 'Ctrl+Shift+F', 'Ctrl+Backquote', 'Ctrl+B', 'Ctrl+J',
    'Ctrl+Comma', 'Ctrl+Shift+F12', 'Alt+ArrowLeft', 'Alt+ArrowRight')))
JETBRAINS_KEYS = {**CODE_KEYS, 'run': 'Shift+F10', 'format': 'Ctrl+Alt+L',
    'files': 'Ctrl+Shift+N', 'terminal': 'Alt+F12', 'sidebar': 'Alt+1', 'settings': 'Ctrl+Alt+S'}
RESERVED = {'Ctrl+W', 'Ctrl+T', 'Ctrl+N', 'Ctrl+R', 'Ctrl+L', 'Ctrl+Tab',
            'Ctrl+Shift+W', 'Ctrl+Shift+T', 'Ctrl+Shift+N', 'Alt+F4', 'Ctrl+Alt+Delete'}
# Ctrl+Shift+N is an intentional JetBrains default and is handled in capture phase.
RESERVED.discard('Ctrl+Shift+N')

class ConfigModel(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True)

class IDEPreferences(ConfigModel):
    theme: Literal['inherit', 'forge', 'code', 'graphite', 'nord', 'midnight', 'paper'] = 'inherit'
    accent: str = Field(default='#68c6ff', pattern=r'^#[0-9a-fA-F]{6}$')
    density: Literal['compact', 'comfortable'] = 'compact'
    sidebarSide: Literal['left', 'right'] = 'left'
    sidebarWidth: int = Field(default=248, ge=180, le=480)
    panelPosition: Literal['bottom', 'right'] = 'bottom'
    panelHeight: int = Field(default=230, ge=140, le=600)
    panelWidth: int = Field(default=400, ge=240, le=640)
    activityBar: bool = True
    statusBar: bool = True
    breadcrumbs: bool = True
    centered: bool = False
    fontFamily: Literal['cascadia', 'consolas', 'jetbrains', 'fira', 'monospace'] = 'cascadia'
    ligatures: bool = True
    lineHeight: float = Field(default=1.6, ge=1.2, le=2.0)
    tabSize: Literal[2, 4, 8] = 4
    insertSpaces: bool = True
    wordWrap: Literal['on', 'off', 'bounded'] = 'off'
    lineNumbers: Literal['on', 'off', 'relative'] = 'on'
    whitespace: Literal['none', 'selection', 'all'] = 'selection'
    smoothScrolling: bool = True
    cursorStyle: Literal['line', 'block', 'underline'] = 'line'
    cursorBlinking: Literal['blink', 'smooth', 'solid'] = 'smooth'
    bracketColors: bool = True
    indentGuides: bool = True
    stickyScroll: bool = False
    keymap: Literal['code', 'jetbrains'] = 'code'
    shortcuts: dict[str, str] = Field(default_factory=dict, max_length=14)
    colors: dict[str, str] = Field(default_factory=dict, max_length=6)

    @field_validator('colors')
    @classmethod
    def validate_colors(cls, value):
        for name, color in value.items():
            if name not in {'background', 'panel', 'editor', 'text', 'muted', 'border'} or not re.fullmatch(r'#[0-9a-fA-F]{6}', color):
                raise ValueError('Only known color tokens and six-digit hex colors are allowed')
        return value

    @field_validator('shortcuts')
    @classmethod
    def validate_shortcuts(cls, value):
        key = r'(?:[A-Z0-9]|F(?:[1-9]|1[0-2])|Enter|Backslash|Backquote|Comma|Period|ArrowLeft|ArrowRight)'
        for command, shortcut in value.items():
            if command not in COMMANDS:
                raise ValueError('Unknown command')
            if shortcut == '':  # Explicitly unbound.
                continue
            if (not re.fullmatch(r'(?:Ctrl\+)?(?:Alt\+)?(?:Shift\+)?' + key, shortcut)
                or not ('Ctrl+' in shortcut or 'Alt+' in shortcut or re.search(r'F\d+$', shortcut))
                or shortcut in RESERVED or shortcut == 'F1'):
                raise ValueError('Invalid or reserved shortcut: ' + shortcut)
        return value

    @model_validator(mode='after')
    def unique_shortcuts(self):
        effective = {**(CODE_KEYS if self.keymap == 'code' else JETBRAINS_KEYS), **self.shortcuts}
        bindings = [s for s in effective.values() if s]
        if len(set(bindings)) != len(bindings):
            raise ValueError('Two commands cannot use the same shortcut')
        return self

class IDEProfilePreferences(ConfigModel):
    theme: Literal['dark', 'light'] = 'dark'
    fontSize: int = Field(default=14, ge=12, le=24)
    minimap: bool = False
    inlineCompletion: bool = True
    ide: IDEPreferences = Field(default_factory=IDEPreferences)

class IDEProfile(ConfigModel):
    id: str = Field(pattern=r'^[a-zA-Z0-9_-]{1,64}$')
    name: str = Field(min_length=1, max_length=60)
    preferences: IDEProfilePreferences

    @field_validator('name')
    @classmethod
    def nonblank_name(cls, name):
        if not name.strip() or any(ord(c) < 32 for c in name):
            raise ValueError('Profile name must be visible text')
        return name.strip()

class IDEProfileDocument(ConfigModel):
    format: Literal['devforge.ide-profile'] = 'devforge.ide-profile'
    version: Literal[1] = 1
    profile: IDEProfile
