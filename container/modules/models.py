from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, RootModel


class Label(BaseModel):
    ja: str
    en: str


class Schema(BaseModel):
    type: str
    format: str | None = Field(default=None)


class ChildItem(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    name: Label
    schema_: Schema = Field(alias="schema")
    unit: str | None = Field(default=None)
    description: str | None = Field(default=None)
    uri: str | None = Field(default=None)
    mode: str | None = Field(default=None)
    order: str | None = Field(default=None)
    original_name: str | None = Field(default=None, alias="originalName")


class MetaDataDef(RootModel):
    root: dict[str, ChildItem]


class Basic(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    date_submitted: str | None = Field(default=None, alias="dateSubmitted")
    data_ownerid: str | None = Field(default=None, alias="dataOwnerId")
    data_name: str | None = Field(default=None, alias="dataName")
    instrument_id: str | None = Field(default=None, alias="instrumentId")
    experiment_id: str | None = Field(default=None, alias="experimentId")
    description: str | None = Field(default=None, alias="description")


class Custom(BaseModel):
    key1: str | None
    key2: str | None
    key3: str | None
    key4: str | None
    key5: str | None
    key6: str | None
    key7: str | None
    key8: str | None
    key9: str | None
    key10: str | None


class Sample(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    sample_id: str | None = Field(default=None, alias="sampleId")
    names: list[str]
    composition: str | None
    reference_url: str | None = Field(default=None, alias="referenceUrl")
    description: str | None
    owner_id: str | None = Field(default=None, alias="ownerId")


class InvoiceJson(BaseModel):
    model_config = ConfigDict(extra='allow', populate_by_name=True)
    dataset_id: str | None = Field(default=None, alias="datasetId")
    basic: Basic
    custom: Custom
    sample: Sample

    def to_json(self, path: Path) -> dict[str, Any]:
        """Convert the InvoiceJson object to a JSON string.

        Returns:
            str: The JSON string representation of the InvoiceJson object.

        """
        with path.open('w', encoding='utf-8') as f:
            json.dump(self.model_dump(by_alias=True), f, ensure_ascii=False, indent=2)

        return self.model_dump(by_alias=True)
