from pathlib import Path

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
