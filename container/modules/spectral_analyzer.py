from __future__ import annotations

from pathlib import Path

import hyperspy._signals as hs_signals
import hyperspy.api as hs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from rdetoolkit.errors import catch_exception_with_message
from rdetoolkit.exceptions import StructuredError
from rdetoolkit.models.rde2types import RdeOutputResourcePath

from modules.interfaces import ISpectralAnalizer


class SpectralAnalizer(ISpectralAnalizer):
    """Abstract base class for HyperSpy2 spectral analyzers."""

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)

    @catch_exception_with_message(error_message="Error: Could not parse em data.")
    def parse(self) -> tuple[np.ndarray, pd.DataFrame]:
        """Read and parse data files.

        Extracts metadata and measurement data.

        Args:
            None

        Returns:
            tuple: A tuple containing the metadata and measurements extracted
            from the file.

        """
        data = self.signal.data
        original_metadata = self._extract_original_metadata(self.signal)
        return data, original_metadata

    def visualize(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualize the data in a spectrum or hologram format based on the file type.

        This function checks if the input file is a spectral data file and,
        if so, calls the `visualize_spectral` method to generate a spectrum
        visualization. Otherwise, it calls the `visualize_hologram` method to
        generate a hologram visualization.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

        Returns:
            None

        """
        if self.is_spectral(self.file_path):
            self.visualize_spectral(resource_paths)
        else:
            self.visualize_hologram(resource_paths)

    def visualize_hologram(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualizes a hologram image based on the input data file.

        This function saves three images to the output resources directory
        using the `save_image`, `save_modified_image`,
        and `save_contrast_adjusted_image` methods, respectively.
        The first method saves an unmodified TIFF image with the same name as
        the input data file. The second method saves a PNG image with the same
        name as the input data file but with the ".png" extension. Finally,
        the third method saves a contrast-adjusted PNG image with the same name
        as the input data file but with the "_conv.png" extension.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

        Returns:
            None

        """
        self.save_image(resource_paths.struct.joinpath(f"{self.file_path.stem}.tif"))
        self.save_modified_image(resource_paths.other_image.joinpath(f"{self.file_path.stem}.png"))
        self.save_contrast_adjusted_image(resource_paths.main_image.joinpath(f"{self.file_path.stem}_conv.png"))

    def visualize_spectral(self, resource_paths: RdeOutputResourcePath) -> None:
        """Visualizes a spectral line graph based on the input data file.

        This function saves a PNG image to the output resources directory using
        the `save_line_graph` method. The image is generated from the data in
        the input data file and has the same name as the input data file but
        with the ".png" extension.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

        Returns:
            None

        """
        self.save_line_graph(resource_paths.main_image.joinpath(f"{self.file_path.stem}.png"))

    @catch_exception_with_message(error_message="Error: Could not save image data.")
    def save_image(self, save_path: Path) -> None:
        """Save as image file.

        Args:
            save_path (Path): Image file path. The extention must be tif.

        Raises:
            StructuredError: An exception is raised if image file conversion fails.

        """
        self.signal.save(save_path)

    @catch_exception_with_message(error_message="Error: Could not plotting data.")
    def save_modified_image(self, save_path: Path) -> None:
        """Save the modified image based on the input data file.

        This function saves an image to the output resources directory using
        the `savefig` method from the `matplotlib` library. The image is
        generated from the data in the input data file and has the same name
        as the input data file but with the ".png" extension.

        Args:
            save_path (Path): The path to the output resources directory for
            the visualization.

        Returns:
            StructuredError: An exception is raised if image file conversion fails.

        """
        self.signal.plot()
        plt.savefig(save_path)
        plt.clf()
        plt.close()

    @catch_exception_with_message(
        error_message="Error: Could not save contrast-adjusted image data.")
    def save_contrast_adjusted_image(self, save_path: Path) -> None:
        """Save contrast-adjusted image based on the input data file.

        This function saves an image to the output resources directory using
        the `savefig` method from the `matplotlib` library. The image is
        generated from the data in the input data file and has the same name
        as the input data file but with the "_conv.png" extension.
        Additionally, a contrast adjustment is made to the image data before
        saving it.

        Args:
            save_path (Path): The path to the output resources directory for
            the visualization.

        Returns:
            StructuredError: An exception is raised if image file conversion
            fails.

        """
        data = self.signal.data
        vmin, vmax = np.percentile(data, [1, 99])

        self.signal.plot()
        if np.max(data) / 2. > np.mean(data):
            self.signal.plot(vmin=vmin, vmax=vmax)
        else:
            self.signal.plot()
        plt.savefig(save_path)
        plt.clf()
        plt.close()

    @catch_exception_with_message(error_message="Error: Could not save image data.")
    def save_line_graph(self, save_path: Path) -> None:
        """Save line graph of the input signal data to the specified file path.

        This function saves a line graph of the input signal data to the
        specified file path using the `plot_spectra` method from
        the `hyperspy.api.plot` library. The y-axis is set to log scale and
        the title is generated based on the file name. Finally, the plot is
        saved as an image file with the same name as the file path but with
        a ".png" extension.

        Args:
            save_path (Path): The path to the output resources directory for the visualization.

        Raises:
            StructuredError: An exception is raised if image file conversion fails.

        """
        ax = hs.plot.plot_spectra(self.signal)
        ax.set_yscale('log')
        ax.set_title(self._set_title_from_filename(self.file_path))
        plt.savefig(save_path)
        plt.clf()
        plt.close()

    def _extract_original_metadata(self, signal: hs.signals.BaseSignal) -> pd.DataFrame:
        """Extract the original metadata from the signal object and converts it to a DataFrame type.

        Args:
            signal (hs.signals.BaseSignal): BaseSignal object extracted from
            em file.

        Returns:
            pd.DataFrame: original_metadata converted to pandas DataFrame type.
            No index.

        """
        try:
            dic = signal.original_metadata.as_dictionary()
            df = pd.json_normalize(dic)
            df = df.T
            df.reset_index(inplace=True)
            df.columns = ['key', 'value']
            self.df_metadata = df
        except Exception as e:
            error_message = "Failed to extract or convert the original_metadata."
            raise StructuredError(error_message) from e
        return self.df_metadata

    def _extract_value_from_metadata(
            self,
            tag: str,
            metadata: pd.DataFrame) -> str | None:
        value: str | None = None
        filtered_row = metadata[metadata['key'] == tag]
        if not filtered_row.empty:
            value = filtered_row['value'].iloc[-1]
        return value

    def _set_title_from_filename(self, filepath: str | Path) -> str:
        if isinstance(filepath, str):
            filepath = Path(filepath)
        return filepath.stem

    @staticmethod
    def is_spectral(input_path: Path) -> bool:
        """Determine whether the input raw file is spectral data or not.

        This function uses the `hs.load` method to load the input raw file and
        check if it contains spectral data. If the loaded signal is an instance
        of the `hs_signals.signal1d.Signal1D` class, the function returns True.
        Otherwise, it raises a `StructuredError` exception with a custom error
        message indicating that the input raw file is not valid.

        Args:
            input_path (Path): The path to the input raw file.

        Returns:
            bool: True if the input raw file contains spectral data,
            False otherwise.

        Raises:
            StructuredError: If the input raw file is not valid or does not
            contain spectral data.

        """
        try:
            s = hs.load(input_path)
            if isinstance(s, hs_signals.signal1d.Signal1D):
                return True
        except Exception:
            err_msg = f"Invalid raw file: {input_path}"
            raise StructuredError(err_msg) from None
        return False
