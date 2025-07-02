from __future__ import annotations

from pathlib import Path

from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules.modules_em.spectral_analyzer import SpectralAnalizer as EmSpectralAnalizer


class SpectralAnalizer(EmSpectralAnalizer):
    """Template class for analysing electron microscopy data files in image formats."""

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    def visualize(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualize the measurement data.

        This function converts the input image file to the required format and
        saves it.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the
            RDE resources.

        Returns:
            None

        """
        self.save_image(resource_paths.main_image.joinpath(f"{self.file_path.stem}.png"))
