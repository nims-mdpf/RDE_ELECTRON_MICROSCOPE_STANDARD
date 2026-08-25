from __future__ import annotations

from pathlib import Path
from typing import Any

from rdetoolkit.models.rde2types import MetaType, RepeatedMetaType

from modules.modules_temdm3.meta_handler import MetaParser as TemDm3MetaParser


class MetaParser(TemDm3MetaParser):
    """Class for parsing and saving metadata.

    This class is for parsing pre-acquired metadata and saving it to a file.
    It only handles constant metadata and does not support repeated metadata.

    Attributes:
        prefix_meta (str): Prefix of the item title of the json data.

    """

    PREFIX_META = 'eels'

    def __init__(self) -> None:
        super().__init__()
        self.prefix_meta = self.PREFIX_META

    def parse(
        self,
        data: dict[str, Any],
        metadata_def_path: Path,
    ) -> tuple[MetaType, RepeatedMetaType | None]:
        """Parse the input data and extract the metadata.

        This function parses the input data dictionary and extracts the
        metadata according to the specified metadata definition file. It first
        assigns default values to any missing metadata fields, then retrieves
        the metadata from the input data using a metadata definition file.
        The retrieved metadata is then assigned to the appropriate attribute of
        the class.

        Args:
            data (dict[str, Any]): The input data dictionary.
            metadata_def_path (Path): The path to the metadata definition file.

        Returns:
            tuple[MetaType, RepeatedMetaType | None]: A tuple containing the
            constant metadata and repeated metadata extracted from the input
            data, if any.

        Raises:
            ValueError: If the input data is missing a required field or has
            an invalid value for one of the fields.

        """
        self._assign_defalut_val(data)
        _meta = self._get_dict_meta(data, metadata_def_path)

        datetime: str | None = self.get_operation_datetime(data)
        self._assign_operation_datetime(_meta, datetime)
        self._assign_measurement_technique(_meta, data)

        self.const_meta_info: MetaType = _meta
        self.repeated_meta_info: RepeatedMetaType | None = None

        return self.const_meta_info, self.repeated_meta_info

    def _assign_measurement_technique(
        self,
        _meta: dict[str, Any],
        data: dict[str, Any],
    ) -> None:
        _key = 'ImageList.TagGroup0.ImageTags.Meta Data.Signal'
        if data.get(_key) is not None:
            _meta['measurement_technique'] = data[_key]

    def get_operation_datetime(
        self,
        data: dict[str, Any],
    ) -> str | None:
        """Get the date and time of the EELS operation.

        This function extracts the date and time from the metadata in a input
        file. It first retrieves the relevant metadata from the input
        dictionary using the specified keys, then converts it to a datetime
        string with the format "YYYY-MM-DD HH:MM:SS". If the metadata does not
        exist, it returns None.

        Args:
            data (dict[str, Any]): The measurement data extracted from the
            input file.

        Returns:
            str | None: The date and time of the EELS operation, or None if
            they cannot be determined.

        """
        date_key = "ImageList.TagGroup0.ImageTags.EELS.Acquisition.Date"
        time_key = "ImageList.TagGroup0.ImageTags.EELS.Acquisition.End time"
        return self._convert_to_datetime_format(data, date_key, time_key)
