from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

import hyperspy.api as hs
import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import MetaType, RdeOutputResourcePath, RepeatedMetaType
from rdetoolkit.rde2util import Meta


class IStructuredDataProcessor(ABC):
    """Abstract base class (interface) for structured data parsers.

    This interface defines the contract that structured data parser
    implementations must follow. The parsers are expected to transform
    structured data, such as DataFrame, into various desired output formats.

    Methods:
        to_csv: A method that saves the given data to a CSV file.

    Implementers of this interface could transform data into various
    formats like CSV, Excel, JSON, etc.

    """

    @abstractmethod
    def to_csv(  # noqa: D102
            self,
            dataframe: pd.DataFrame,
            save_path: Path,
            *,
            header: list[str] | None = None) -> Any:
        raise NotImplementedError


class IMetaParser(ABC):
    """Abstract base class (interface) for meta information parsers.

    This interface defines the contract that meta information parser
    implementations must follow. The parsers are expected to save the
    constant and repeated meta information to a specified path.

    Method:
        save_meta: Saves the constant and repeated meta information to a specified path.
        parse: This method returns two types of metadata: const_meta_info and repeated_meta_info.

    """

    @abstractmethod
    def parse(
        self,
        data: dict[str, Any],
        metadata_def_path: Path,
    ) -> tuple[MetaType, RepeatedMetaType | None]:
        """Parse the input data and returns a tuple containing the MetaType and RepeatedMetaType objects.

        This function parses the input data dictionary using the provided
        metadata definition path and returns a tuple containing the MetaType
        and RepeatedMetaType objects. If an error occurs during parsing,
        it raises a ValueError exception.

        Args:
            data (dict[str, Any]): The input data to be parsed.
            metadata_def_path (Path): The path to the metadata definition file.

        Returns:
            tuple[MetaType, RepeatedMetaType | None]: A tuple containing
            the MetaType and RepeatedMetaType objects. If no repeated metadata is found,
            returns a tuple with only the MetaType object.

        Raises:
            ValueError: If an error occurs during parsing.

        """
        raise NotImplementedError

    @abstractmethod
    def save_meta(
            self,
            save_path: Path,
            meta: Meta,
            *,
            const_meta_info: MetaType | None = None,
            repeated_meta_info: RepeatedMetaType | None = None) -> Any:
        """Save the constant and repeated meta information to a specified path.

        Args:
            save_path (Path): The path where the meta information will be saved.
            meta (Meta): The meta information to be saved.
            const_meta_info (MetaType, optional): Constant meta information. Defaults to None.
            repeated_meta_info (RepeatedMetaType, optional): Repeated meta information. Defaults to None.

        """
        raise NotImplementedError


class ISpectralAnalizer(ABC):
    """Abstract base class for HyperSpy2 spectral analyzers.

    This abstract base class provides a structure for spectral analyzers using HyperSpy2. It defines methods for parsing and visualizing data, as well as a constructor that initializes the signal object based on the provided file path.

    Args:
        file_path (Path): The path to the input file.

    Attributes:
        file_path (Path): The path to the input file.
        signal (hs.signals.BaseSignal): The HyperSpy2 signal object representing the data in the input file.

    Raises:
        StructuredError: If an error occurs during parsing or visualization.

    """

    @abstractmethod
    def __init__(self, file_path: Path) -> None:
        self.file_path: Path = file_path
        try:
            self.signal: hs.signals.BaseSignal = hs.load(file_path)
        except NotImplementedError as e:
            error_message = ("The input file could not be loaded.")
            raise StructuredError(emsg=error_message, ecode=1) from e

    @abstractmethod
    def parse(self) -> Any:  # noqa: ANN201, D102
        """Parse input files and extract metadata."""
        raise NotImplementedError

    @abstractmethod
    def visualize(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualizing Signals.

        Args:
        resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

        """
        raise NotImplementedError
