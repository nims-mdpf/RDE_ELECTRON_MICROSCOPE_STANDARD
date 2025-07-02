from __future__ import annotations

from pathlib import Path
from typing import Any, cast

import dateutil.parser
from rdetoolkit import rde2util
from rdetoolkit.models.rde2types import MetaType, RepeatedMetaType

from modules.meta_handler import MetaParser as MainMetaParser


class MetaParser(MainMetaParser):
    """Class for parsing and saving metadata.

    This class is for parsing pre-acquired metadata and saving it to a file.
    It only handles constant metadata and does not support repeated metadata.

    Attributes:
        prefix_meta (str): Prefix of the item title of the json data.

    """

    def __init__(self) -> None:
        super().__init__()
        self.prefix_meta: str

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
        The retrieved metadata is then assigned to the appropriate attribute
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
        self._assign_pixel_actual_size_along_axes(_meta)
        self._assign_measurement_technique(_meta, data)

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
            metaobj (rde2util.Meta): The meta object containing the information to be saved.
            const_meta_info (Optional[MetaType], optional): The constant meta information to be used. Defaults to None.
            repeated_meta_info (RepeatedMetaType | None, optional): The repeated meta information. Defaults to None.

        Returns:
            assign_meta_info: The assigned meta information.

        """
        _const_meta_info = self.const_meta_info if const_meta_info is None else const_meta_info
        if repeated_meta_info is not None:
            error_message = "Repeated meta info is not supported in this template"
            raise NotImplementedError(error_message)

        metaobj.assign_vals(_const_meta_info)

        return cast(rde2util.Meta, metaobj.writefile(str(save_path)))

    def _assign_operation_datetime(
        self,
        _meta: dict[str, Any],
        datetime: str | None,
    ) -> None:
        if datetime is None:
            return
        prefix = self.prefix_meta.lower()
        parsed_datetime = dateutil.parser.parse(datetime)
        _meta[f'{prefix}.operation_date_time_year'] = parsed_datetime.strftime("%Y")
        _meta[f'{prefix}.operation_date_time_month'] = parsed_datetime.strftime("%m")
        _meta[f'{prefix}.operation_date_time_day'] = parsed_datetime.strftime("%d")
        _meta[f'{prefix}.operation_date_time_hour'] = parsed_datetime.strftime("%H")
        _meta[f'{prefix}.operation_date_time_minute'] = parsed_datetime.strftime("%M")
        _meta[f'{prefix}.operation_date_time_second'] = parsed_datetime.strftime("%S")

    def _assign_pixel_actual_size_along_axes(
        self,
        _meta: dict[str, Any],
    ) -> None:
        prefix = self.prefix_meta.lower()
        if _meta.get(f'{prefix}.pixel_number_along_x_axis') is not None and \
                _meta.get(f'{prefix}.pixel_number_along_x_axis') is not None:
            _meta[f'{prefix}.x_axis'] = str(
                int(_meta[f'{prefix}.pixel_number_along_x_axis'])
                * float(_meta[f'{prefix}.pixel_size_along_x_axis']),
            )
        if _meta.get(f'{prefix}.pixel_number_along_y_axis') is not None and \
                _meta.get(f'{prefix}.pixel_number_along_y_axis') is not None:
            _meta[f'{prefix}.pixel_actual_size_along_y_axis'] = str(
                int(_meta[f'{prefix}.pixel_number_along_y_axis'])
                * float(_meta[f'{prefix}.pixel_size_along_y_axis']),
            )

    def _assign_measurement_technique(
        self,
        _meta: dict[str, Any],
        data: dict[str, Any],
    ) -> None:
        if data.get('ImageList.TagGroup0.ImageTags.Microscope Info.Illumination Mode') is None:
            return
        _meta['measurement_technique'] = \
            data['ImageList.TagGroup0.ImageTags.Microscope Info.Illumination Mode']

    def _assign_defalut_val(self, data: dict[str, Any]) -> None:
        if data.get('ImageList.TagGroup0.ImageData.Calibrations.Brightness.Units') is None:
            data['ImageList.TagGroup0.ImageData.Calibrations.Brightness.Units'] = ''
        if data.get('ImageList.TagGroup0.ImageTags.Session Info.Specimen') is None:
            data['ImageList.TagGroup0.ImageTags.Session Info.Specimen'] = 'legend'

    def get_operation_datetime(
        self,
        data: dict[str, Any],
    ) -> str | None:
        """Get the date and time of the TEM, STEM, and TED operation.

        This function extracts the date and time from the metadata in a input
        file. It first retrieves the relevant metadata from the input
        dictionary using the specified keys, then converts it to a datetime
        string with the format "YYYY-MM-DD HH:MM:SS". If the metadata does not
        exist, it returns None.

        Args:
            data (dict[str, Any]): The measurement data extracted from the
            input file.

        Returns:
            str | None: The date and time of the TEM, STEM, and TED operation,
            or None if they cannot be determined.

        """
        date_key = "ImageList.TagGroup0.ImageTags.DataBar.Acquisition Date"
        time_key = "ImageList.TagGroup0.ImageTags.DataBar.Acquisition Time"
        return self._convert_to_datetime_format(data, date_key, time_key)

    def _convert_to_datetime_format(
        self,
        data: dict[str, Any],
        date_key: str,
        time_key: str,
    ) -> str | None:
        if data.get(date_key) is None or data.get(time_key) is None:
            return None
        return " ".join([str(data[date_key]), str(data[time_key])])
