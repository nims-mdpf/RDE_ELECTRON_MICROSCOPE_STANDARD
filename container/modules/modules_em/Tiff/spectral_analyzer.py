from __future__ import annotations

from pathlib import Path

from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules.modules_em.spectral_analyzer import SpectralAnalizer as EmSpectralAnalizer


class SpectralAnalizer(EmSpectralAnalizer):
    """Template class for analysing electron microscopy data files in Tiff format."""

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    def visualize(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualize the measurement data.

        This function visualizes the image using a modified version of the
        original image and saves it to the specified output path.

        Args:
            resource_paths (RdeOutputResourcePath): The resource paths for the
            output files.

        Returns:
            None

        """
        self.save_modified_image(
            resource_paths.other_image.joinpath(f"{self.file_path.stem}.png"),
        )
        self.save_contrast_adjusted_image(
            resource_paths.main_image.joinpath(f"{self.file_path.stem}_conv.png"),
        )
