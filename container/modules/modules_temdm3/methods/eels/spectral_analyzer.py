from pathlib import Path

from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules.modules_temdm3.spectral_analyzer import SpectralAnalizer as TemDm3SpectralAnalizer


class SpectralAnalyzer(TemDm3SpectralAnalizer):
    """A class for visualizing measurement data.

    This class provides a set of methods for visualizing the results of
    measurements, such as holograms and spectra. It is a child class of
    TemDm3SpectralAnalizer, which is used to analyze the spectral data from
    measurements.
    """

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    def visualize(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualizes a spectral line graph based on the input data file.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

        Returns:
            None

        """
        self.visualize_spectral(resource_paths)
