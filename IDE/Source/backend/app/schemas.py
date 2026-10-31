import re
from typing import Any, Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, field_validator
from .ide_settings import IDEPreferences, IDEProfile

class StrictModel(BaseModel):
    model_config = ConfigDict(extra='forbid')

class FileIn(StrictModel):
    name: str = Field(min_length=1, max_length=100)
    content: str = Field(max_length=200_000)

    @field_validator('name')
    @classmethod
    def safe_name(cls, value: str) -> str:
        if not re.fullmatch(r'[\w-][\w. -]*\.(py|sql|html|css|c|h|js|ts|java|cpp|hpp|cc|cxx|cs|m|rs|bsl|lua|asm|s|inc|md|txt|json)', value) or '..' in value:
            raise ValueError('Invalid filename or unsupported extension')
        return value

class ProjectIn(StrictModel):
    name: str = Field(min_length=1, max_length=80)
    language: Literal['python', 'sql', 'postgresql', 'html-css', 'c', 'javascript', 'typescript', 'java', 'cpp', 'csharp', 'objc', 'rust', '1c', 'lua', 'assembly']
    files: list[FileIn] = Field(min_length=1, max_length=30)
    revision: int = Field(default=1, ge=1)

    @field_validator('name')
    @classmethod
    def nonblank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError('Name cannot be blank')
        return value.strip()

    @field_validator('files')
    @classmethod
    def unique_files(cls, files: list[FileIn]) -> list[FileIn]:
        if len({f.name.casefold() for f in files}) != len(files):
            raise ValueError('File names must be unique')
        return files

class ResultIn(StrictModel):
    id: str = Field(max_length=80)
    actual: Any = None
    error: str | None = Field(default=None, max_length=10000)

class AttemptIn(StrictModel):
    id: UUID
    lesson_id: str = Field(max_length=80)
    results: list[ResultIn] = Field(max_length=20)

class SettingsIn(StrictModel):
    theme: Literal['dark', 'light'] = 'dark'
    fontSize: int = Field(default=14, ge=12, le=24)
    mode: Literal['learning', 'developer'] = 'learning'
    lastLesson: str | None = Field(default=None, max_length=80)
    aiProvider: Literal['disabled','ollama','lmstudio','openai-local'] = 'disabled'
    aiPort: int = Field(default=11434, ge=1024, le=65535)
    aiModel: str = Field(default='',max_length=120)
    inlineCompletion: bool = True
    aiCompletion: bool = False
    minimap: bool = False
    ide: IDEPreferences = Field(default_factory=IDEPreferences)
    ideProfiles: list[IDEProfile] = Field(default_factory=list, max_length=12)

    @field_validator('ideProfiles')
    @classmethod
    def unique_profiles(cls, profiles):
        if len({p.id for p in profiles}) != len(profiles) or len({p.name.casefold() for p in profiles}) != len(profiles):
            raise ValueError('Profile IDs and names must be unique')
        return profiles

class DraftIn(StrictModel):
    code: str = Field(max_length=200_000)
