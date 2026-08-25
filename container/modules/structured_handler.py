from __future__ import annotations

from pathlib import Path

import pandas as pd
from rdetoolkit.errors import catch_exception_with_message

from modules.interfaces import IStructuredDataProcessor


class StructuredDataProcessor(IStructuredDataProcessor):
    """Class for handling header and data information.

    This class saves metadata information extracted from the input file as
    a CSV files.

    """

    def to_csv(
        self,
        dataframe: pd.DataFrame,
        save_path: Path,
        *,
        header: list[str] | None = None,
    ) -> None:
        """Save the given DataFrame to a CSV file.

        Args:
            dataframe (pd.DataFrame): The data to save.
            save_path (Path): The path where the CSV file will be saved.
            header (Optional[list[str]]): The header for the CSV file. Defaults to None.

        """
        if header is not None:
            dataframe.to_csv(save_path, header=header, index=False)
        else:
            dataframe.to_csv(save_path, index=False)

    @catch_exception_with_message(error_message="Error: Could not save a metadata csv file.")
    def save_csv(self, metadata: pd.DataFrame, save_path: Path) -> None:
        """Save the input metadata to a CSV file at the specified path.

        This function saves the input metadata to a CSV file at the specified
        path using the `to_csv` method from the `pandas` library. The output
        is a CSV file with no header and no index. Finally, the resulting CSV
        file is saved to the specified path.

        Args:
            metadata (pd.DataFrame): The metadata to be saved. Must be a
            pandas DataFrame object.
            save_path (Path): The path to the output CSV file.

        Returns:
            None

        Raises:
            TypeError: If the `metadata` argument is not a pandas DataFrame
            object.

        """
        self.to_csv(metadata, save_path, header=None)
