from __future__ import annotations

from pathlib import Path
from typing import Any

from rdetoolkit.exceptions import StructuredError

from modules.modules_em.DigitalMicrograph.spectral_analyzer import SpectralAnalizer as DmSpectralAnalizer
from modules.modules_em.ImageFormats.spectral_analyzer import SpectralAnalizer as ImageSpectralAnalizer
from modules.modules_em.meta_handler import MetaParser
from modules.modules_em.Tiff.spectral_analyzer import SpectralAnalizer as TiffSpectralAnalizer
from modules.structured_handler import StructuredDataProcessor

FILETYPE_EXTENTION_MAPPING = {
    '.png': 'Image',
    '.bmp': 'Image',
    '.dib': 'Image',
    '.gif': 'Image',
    '.jpeg': 'Image',
    '.jpe': 'Image',
    '.jpg': 'Image',
    '.tif': 'Tiff',
    '.tiff': 'Tiff',
    '.dm3': 'DigitalMicrograph',
    '.dm4': 'DigitalMicrograph',
}

FILETYPE_SPECIFIC_INFO_MAPPING = {
    'Image': (ImageSpectralAnalizer, 'metadata-def_Image.json'),
    'Tiff': (TiffSpectralAnalizer, 'metadata-def_Tiff.json'),
    'DigitalMicrograph': (DmSpectralAnalizer, 'metadata-def_DigitalMicrograph.json'),
}


class EmFactory:
    """The EmFactory class provides a way to create Em objects from different types of files.

    The EmFactory class takes in an input file, a task support directory,
    and a configuration dictionary as arguments during initialization.
    It then uses these values to determine the type of file and retrieve
    the corresponding class for spectral analyzers. Finally, it initializes
    the EmFactory object with the MetaParser and StructuredDataProcessor classes,
    as well as the spectral analyzer class for the given file type.
    """

    def __init__(
        self,
        meta_parser: Any,
        structured_processor: StructuredDataProcessor,
        spectral_analizer: Any,
    ):
        self.meta_parser = meta_parser
        self.structured_processor = structured_processor
        self.spectral_analizer = spectral_analizer

    @staticmethod
    def get_objects(
        rawfile: Path,
        path_tasksupport: Path,
    ) -> tuple[Path, EmFactory]:
        """Get the necessary objects for the spectral analysis process.

        This function gets the necessary objects for the spectral analysis
        process based on the provided input file and configuration.
        The function first extracts the suffix of the input file, then uses
        this value to determine the type of file and retrieve the corresponding
        class for spectral analyzers. It then initializes the EmFactory object
        with the MetaParser and StructuredDataProcessor classes, as well as
        the spectral analyzer class for the given file type. Finally,
        it returns a tuple containing the metadata definition file and
        the EmFactory object.

        Args:
            rawfile (Path): The path to the input file.
            path_tasksupport (Path): The path to the task support directory.

        Returns:
            tuple[Path, EmFactory]: A tuple containing the metadata definition
            file and the EmFactory object.

        Raises:
            StructuredError: If an error occurs during parsing or visualization.

        """
        suffix = rawfile.suffix.lower()

        try:
            filetype = FILETYPE_EXTENTION_MAPPING[suffix]
        except KeyError:
            err_msg = f"Non-supported extensions: {rawfile}"
            raise StructuredError(err_msg) from None

        try:
            class_spectralanalizer, metadata_def_filename = FILETYPE_SPECIFIC_INFO_MAPPING[filetype]
        except KeyError:
            err_msg = f"Non-supported extensions: {rawfile}"
            raise StructuredError(err_msg) from None

        metadata_def = path_tasksupport.joinpath(metadata_def_filename)

        module = EmFactory(
            MetaParser(),
            StructuredDataProcessor(),
            class_spectralanalizer(rawfile),
        )

        return metadata_def, module
