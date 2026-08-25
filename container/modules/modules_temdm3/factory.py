from __future__ import annotations

from pathlib import Path
from typing import Any

from rdetoolkit.exceptions import StructuredError

from modules.modules_temdm3.inputfile_handler import FileReader
from modules.modules_temdm3.invoice_handler import InvoiceWriter
from modules.modules_temdm3.meta_handler import MetaParser
from modules.modules_temdm3.methods.eels.meta_handler import MetaParser as EelsMetaParser
from modules.modules_temdm3.methods.eels.spectral_analyzer import SpectralAnalyzer as EelsSpectralAnalyzer
from modules.modules_temdm3.methods.stem.meta_handler import MetaParser as StemMetaParser
from modules.modules_temdm3.methods.stem.spectral_analyzer import SpectralAnalyzer as StemSpectralAnalyzer
from modules.modules_temdm3.methods.ted.meta_handler import MetaParser as TedMetaParser
from modules.modules_temdm3.methods.ted.spectral_analyzer import SpectralAnalyzer as TedSpectralAnalyzer
from modules.modules_temdm3.methods.tem.meta_handler import MetaParser as TemMetaParser
from modules.modules_temdm3.methods.tem.spectral_analyzer import SpectralAnalyzer as TemSpectralAnalyzer
from modules.modules_temdm3.spectral_analyzer import SpectralAnalizer
from modules.modules_temdm3.spectral_analyzer import SpectralAnalizer as TemDm3SpectralAnalizer
from modules.structured_handler import StructuredDataProcessor

METHOD_CLASS_MAPPING = {
    'TEM': (TemSpectralAnalyzer, TemMetaParser),
    'STEM': (StemSpectralAnalyzer, StemMetaParser),
    'TED': (TedSpectralAnalyzer, TedMetaParser),
    'EELS': (EelsSpectralAnalyzer, EelsMetaParser),
}


class TemDm3Factory:
    """A factory class for creating instances of `TemDm3` objects.

    This class provides a way to create instances of `TemDm3` objects using
    various dependencies. The dependencies are injected through the constructor,
    and the resulting instance can then be used to process raw data files.

    Attributes:
        file_reader (FileReader): An instance of the `FileReader` class that
        reads the input raw data files.
        invoice_writer (InvoiceWriter): An instance of the `InvoiceWriter`
        class that writes the output invoices.
        meta_parser (Any): An instance of the `MetaParser` class that parses
        the metadata from the input raw data files.
        structured_processor (StructuredDataProcessor): An instance of the
        `StructuredDataProcessor` class that processes the structured data
        extracted from the input raw data files.
        spectral_analizer (Any): An instance of the `SpectralAnalizer` class
        that analyzes the spectral data extracted from the input raw data files.

    """

    def __init__(
        self,
        file_reader: FileReader,
        invoice_writer: InvoiceWriter,
        meta_parser: Any,
        structured_processor: StructuredDataProcessor,
        spectral_analizer: Any,
    ):
        """Initialize new instance of the `TemDm3Factory` class.

        Args:
            file_reader (FileReader): An instance of the `FileReader` class
            that reads the input raw data files.
            invoice_writer (InvoiceWriter): An instance of the `InvoiceWriter`
            class that writes the output invoices.
            meta_parser (Any): An instance of the `MetaParser` class that
            parses the metadata from the input raw data files.
            structured_processor (StructuredDataProcessor): An instance of the
            `StructuredDataProcessor` class that processes the structured data
            extracted from the input raw data files.
            spectral_analizer (Any): An instance of the `SpectralAnalizer`
            class that analyzes the spectral data extracted from the input
            raw data files.

        """
        self.file_reader = file_reader
        self.invoice_writer = invoice_writer
        self.meta_parser = meta_parser
        self.structured_processor = structured_processor
        self.spectral_analizer = spectral_analizer

    @staticmethod
    def get_base_objects() -> TemDm3Factory:
        """Return new instance of the `TemDm3Factory` class with default dependencies.

        This function returns a new instance of the `TemDm3Factory` class with
        default dependencies that can be used to process raw data files.
        The resulting object can then be customized and used for processing.

        Returns:
            TemDm3Factory: A new instance of the `TemDm3Factory` class with
            default dependencies.

        """
        return TemDm3Factory(
            FileReader(),
            InvoiceWriter(),
            None,
            StructuredDataProcessor(),
            None,
        )

    def assign_objects_by_method(
        self,
        rawfile: Path,
        path_tasksupport: Path,
    ) -> tuple[Path, Path, str]:
        """Assign modules based on the measurement method from the metadata.

        Args:
            rawfile (Path): The path to the raw file.
            path_tasksupport (Path): The path to the task support directory.

        Returns:
            None

        Raises:
            StructuredError: If the measurement method could not be determined.

        """
        # Identify measurement methods from metadata
        temdm3_spectral_analyzer = TemDm3SpectralAnalizer(rawfile)
        method = temdm3_spectral_analyzer.identify_mesurement_method()
        method = method.upper()

        if method not in METHOD_CLASS_MAPPING:
            error_message = "The measurement method could not be determined."
            raise StructuredError(error_message, 1)

        class_spectralanalizer, class_metaparser = get_classes(method)

        metadata_def = path_tasksupport.joinpath(f"metadata-def_{method}.json")
        default_value = path_tasksupport.joinpath(f"default_value_{method}.csv")

        # Assign modules
        self.meta_parser = class_metaparser()
        self.spectral_analizer = class_spectralanalizer(rawfile)

        return metadata_def, default_value, method


def get_classes(method: str) -> tuple[type[SpectralAnalizer], type[MetaParser]]:
    """Get classes for spectral analyzer and meta parser based on measurement method.

    Args:
        method (str): The measurement method. Must be in uppercase.

    Returns:
        tuple[type[SpectralAnalizer], type[MetaParser]]: A tuple containing
        the class of the spectral analyzer and meta parser for the given
        measurement method.

    Raises:
        StructuredError: If the measurement method is not supported.

    """
    method = method.upper()
    try:
        return METHOD_CLASS_MAPPING[method]
    except KeyError:
        err_msg = f"Unsupported measurement method combinations '{method}'"
        raise StructuredError(err_msg) from None
