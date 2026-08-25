from __future__ import annotations

import pandas as pd
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules.spectral_analyzer import SpectralAnalizer as MainSpectralAnalizer


class SpectralAnalizer(MainSpectralAnalizer):
    """Abstract base class for HyperSpy2 spectral analyzers."""

    def visualize(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualize the data in a hologram format based on the file type.

        This function creates an image file from the measurement data in the
        input file.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

        Returns:
            None

        """
        self.visualize_hologram(resource_paths)

    def identify_mesurement_method(self) -> str:
        """Identify the measurement method used in the input file.

        This function identifies the measurement method used in the input file
        based on the metadata extracted from the file. The function first
        extracts the signal type and operation mode from the metadata, and then
        uses these values to determine the measurement method. If an error
        occurs during this process, it raises a StructuredError exception.

        Args:
            self (object): The input file object.

        Returns:
            str | None: The measured signal type or None if the signal type
            cannot be determined.

        Raises:
            StructuredError: If an error occurs during parsing or visualization.

        """
        metadata: pd.DataFrame = self._extract_original_metadata(self.signal)
        signal = self._extract_value_from_metadata(
            "ImageList.TagGroup0.ImageTags.Meta Data.Signal",
            metadata)
        mode_ope = self._extract_value_from_metadata(
            "ImageList.TagGroup0.ImageTags.Microscope Info.Operation Mode",
            metadata)
        unittag = self._extract_value_from_metadata(
            "ImageList.TagGroup0.ImageData.Calibrations.Dimension.TagGroup0.Units",
            metadata)

        # Determining if Spectrum
        if signal == 'EELS':
            return signal
        if signal == 'X-ray':
            # It is meant to be EDS data.
            error_message = "ERROR: unknown dm3 file type"
            raise StructuredError(error_message)

        # Basic judgment by operation mode
        if mode_ope == 'IMAGING':
            return 'TEM'
        if mode_ope == 'DIFFRACTION':
            return 'TED'

        # Detailed determination of SCANNING mode
        # and Determination of diffraction units
        if mode_ope == 'SCANNING' and unittag in ('1/nm', 'mrad'):
            # It means Diffraction pattern data (DIFF).
            return 'TED'

        # Operation mode is not 'SCANNING', 'IMAGING', or 'DIFFRACTION',
        # treat as STEM (RDE 1.0 compliant)
        return 'STEM'
