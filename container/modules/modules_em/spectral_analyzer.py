from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from rdetoolkit.errors import catch_exception_with_message

from modules.spectral_analyzer import SpectralAnalizer as MainSpectralAnalizer


class SpectralAnalizer(MainSpectralAnalizer):
    """Template class for analysing electron microscopy data."""

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    @catch_exception_with_message(error_message="Error: Could not parse em data.")
    def parse(self) -> tuple[np.ndarray, pd.DataFrame]:
        """Read and parse electron microscopy image data in various formats.

        Args:
            None

        Returns:
            tuple: A tuple containing the metadata and measurements extracted
                from the file.

        """
        data = self.signal.data
        original_metadata = self._extract_original_metadata(self.signal)
        return data, original_metadata

    @catch_exception_with_message(error_message="Error: Could not save image data.")
    def save_image(self, save_path: Path) -> None:
        """Save as an image file.

        Args:
            save_path (Path): Image file path. The extention must be tif.

        Raises:
            StructuredError: An exception is raised if image file conversion fails.

        """
        self.signal.save(save_path)
