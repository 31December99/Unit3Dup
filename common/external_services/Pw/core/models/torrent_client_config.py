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
    configContract: str = ""
    enable: bool = True
    fields: list[Field] = field(default_factory=list)
    id: int = 0
    implementation: str = ""
    implementationName: str = ""
    infoLink: str = ""
    name: str = ""
    priority: int = 0
    protocol: str = ""
    supportsCategories: bool = False
    tags: list[str] = field(default_factory=list)
