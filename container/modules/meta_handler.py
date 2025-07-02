from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from rdetoolkit import rde2util
from rdetoolkit.models.rde2types import MetaType, RepeatedMetaType

from modules.interfaces import IMetaParser
from modules.models import MetaDataDef


class MetaParser(IMetaParser):
    """Parses metadata and saves it to a specified path.

    This class is designed to parse metadata from a dictionary and save it to a specified path using
    a provided Meta object. It can handle both constant and repeated metadata.

    Attributes:
        const_meta_info (MetaType | None): Dictionary to store constant metadata.
        repeated_meta_info (RepeatedMetaType | None): Dictionary to store repeated metadata.
        metadata_def_json_path (Path | None): Path of the metadata_def.json.

    """

    def __init__(self, *, metadata_def_json_path: Path | None = None) -> None:
        self.const_meta_info: MetaType = {}
        self.repeated_meta_info: RepeatedMetaType | None = {}
        self.metadata_def_json_path = metadata_def_json_path

    def save_meta(
        self,
        save_path: Path,
        metaobj: rde2util.Meta,
        *,
        const_meta_info: MetaType | None = None,
        repeated_meta_info: RepeatedMetaType | None = None,
    ) -> rde2util.Meta:
        """Save parsed metadata to a file using the provided Meta object.

        Args:
            save_path (Path): The path where the metadata will be saved.
            metaobj (rde2util.Meta): The Meta object that handles operate of metadata.
            const_meta_info (MetaType | None): The constant metadata to save. Defaults to the
            internal const_meta_info if not provided.
            repeated_meta_info (RepeatedMetaType | None): The repeated metadata to save. Defaults
            to the internal repeated_meta_info if not provided.

        Returns:
            str: The result of the meta assignment operation.

        """
        if const_meta_info is None:
            const_meta_info = self.const_meta_info
        if repeated_meta_info is not None:
            error_message = "Repeated meta info is not supported in this template"
            raise NotImplementedError(error_message)

        metaobj.assign_vals(const_meta_info)

        return cast(rde2util.Meta, metaobj.writefile(str(save_path)))

    def _get_dict_meta(
        self,
        data: dict[str, Any],
        metadata_def_path: Path,
    ) -> dict[str, Any]:
        _meta: dict = {}
        metadef_contents = rde2util.read_from_json_file(metadata_def_path)
        bind_object = MetaDataDef.model_validate(metadef_contents)
        for key, value in bind_object.root.items():
            if value.original_name is None:
                continue
            if data.get(value.original_name) is None:
                continue
            if data[value.original_name] == '[]':
                # An empty string is denoted as '[]'.
                continue
            _meta[key] = str(data[value.original_name])
        return _meta
