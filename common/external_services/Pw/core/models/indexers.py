# -*- coding: utf-8 -*-

from dataclasses import dataclass, field


@dataclass
class SubCategory:
    id: int = 0
    name: str = ''
    subCategories: list[any] = field(default_factory=list)


@dataclass
class Category:
    id: int = 0
    name: str = ''
    subCategories: list[SubCategory] = field(default_factory=list)


@dataclass
class Capability:
    bookSearchParams: list[str] = field(default_factory=list)
    categories: list[Category] = field(default_factory=list)


@dataclass
class FieldOption:
    hint: str = ''
    name: str = ''
    order: int = 0
    value: int = 0


@dataclass
class Field:
    advanced: bool = False
    hidden: str = ''
    isFloat: bool = False
    name: str = ''
    order: int = 0
    privacy: str = ''
    type: str = ''
    value: str = ''
    helpText: str = ''
    label: str = ''
    selectOptionsProviderAction: str = ''
    selectOptions: list[FieldOption] = field(default_factory=list)
    unit: str = ''


@dataclass
class Indexer:
    added: str = ''
    appProfileId: int = 0
    capabilities: Capability = field(default_factory=Capability)
    configContract: str = ''
    definitionName: str = ''
    description: str = ''
    downloadClientId: int = 0
    enable: bool = True
    encoding: str = ''
    fields: list[Field] = field(default_factory=list)
    id: int = 0
    implementation: str = ''
    implementationName: str = ''
    indexerUrls: list[str] = field(default_factory=list)
    infoLink: str = ''
    language: str = ''
    legacyUrls: list[str] = field(default_factory=list)
    name: str = ''
    priority: int = 0
    privacy: str = ''
    protocol: str = ''
    redirect: bool = False
    sortName: str = ''
    supportsPagination: bool = False
    supportsRedirect: bool = False
    supportsRss: bool = False
    supportsSearch: bool = False
    tags: list[int] = field(default_factory=list)
