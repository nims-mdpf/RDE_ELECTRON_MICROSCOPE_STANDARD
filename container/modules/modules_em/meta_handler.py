from __future__ import annotations

from pathlib import Path
from typing import Any, cast

from rdetoolkit import rde2util
from rdetoolkit.models.rde2types import MetaType, RepeatedMetaType

from modules.meta_handler import MetaParser as MainMetaParser


class MetaParser(MainMetaParser):
    """Class for parsing and saving metadata.

    This class is for parsing pre-acquired metadata and saving it to a file.
    It only handles constant metadata and does not support repeated metadata.
    """

    def parse(
        self,
        data: dict[str, Any],
        metadata_def_path: Path,
    ) -> tuple[MetaType, RepeatedMetaType | None]:
        """Parse the input data and extract the metadata.

        This function parses the input data dictionary and extracts the
        metadata according to the specified metadata definition file. It first
        retrieves the metadata from the input data using a metadata definition
        file, then assigns it to the appropriate attribute of the class.

        Args:
            data (dict[str, Any]): Metadata in dictionary format extracted from
            the input file.
            metadata_def_path (Path): The path to the metadata definition file.

        Returns:
            tuple[MetaType, RepeatedMetaType | None]: A tuple containing the
            constant metadata and repeated metadata extracted from the input
            data, if any.

        Raises:
            ValueError: If the input data is missing a required field or has
            an invalid value for one of the fields.

        """
        _meta = self._get_dict_meta(data, metadata_def_path)

        self.const_meta_info: MetaType = _meta
        self.repeated_meta_info: RepeatedMetaType | None = None

        return self.const_meta_info, self.repeated_meta_info

    def save_meta(
        self,
        save_path: Path,
        metaobj: rde2util.Meta,
        *,
        const_meta_info: MetaType | None = None,
        repeated_meta_info: RepeatedMetaType | None = None,
    ) -> rde2util.Meta:
        """Save the meta information to a file.

        Args:
            save_path (Path): The path where the meta information will be saved.
            metaobj (rde2util.Meta): The meta object containing the information
            to be saved.
            const_meta_info (Optional[MetaType], optional): The constant meta
            information to be used. Defaults to None.
            repeated_meta_info (RepeatedMetaType | None, optional): The repeated
            meta information. Defaults to None.

        Returns:
            assign_meta_info: The assigned meta information.

        """
        _const_meta_info = self.const_meta_info if const_meta_info is None else const_meta_info
        if repeated_meta_info is not None:
            error_message = "Repeated meta info is not supported in this template"
            raise NotImplementedError(error_message)

        metaobj.assign_vals(_const_meta_info)

        return cast(rde2util.Meta, metaobj.writefile(str(save_path)))
