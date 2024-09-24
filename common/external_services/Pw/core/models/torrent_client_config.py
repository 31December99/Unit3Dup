# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class SelectOption:
    hint: str
    name: str
    order: int
    value: int


@dataclass
class Field:
    advanced: bool = False
    isFloat: bool = False
    label: str = ""
    name: str = ""
    order: int = 0
    privacy: str = "normal"
    type: str = "textbox"
    value: str | int | bool | None = None
    helpText: str | None = None
    selectOptions: list[SelectOption] | None = None


@dataclass
class TorrentClientConfig:
    categories: list[str] = field(default_factory=list)
    configContract: str | None = None
    enable: bool = True
    fields: list[Field] = field(default_factory=list)
    id: int = 0
    implementation: str | None = None
    implementationName: str | None = None
    infoLink: str | None = None
    name: str | None = None
    priority: int = 0
    protocol: str | None = None
    supportsCategories: bool = False
    tags: list[str] = field(default_factory=list)
