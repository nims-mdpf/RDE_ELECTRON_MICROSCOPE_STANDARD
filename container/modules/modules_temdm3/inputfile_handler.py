import collections
from pathlib import Path

from rdetoolkit.exceptions import StructuredError


class FileReader:

    READABLE_EXTENSIONS = ('.dm3')

    def check_for_consistency(self, rawfiles: tuple[Path, ...]) -> Path:
        """Check if the input files are consistent and return the first file.

        Args:
            rawfiles (tuple[Path, ...]): A tuple of paths to the raw files.
            Must be non-empty.

        Returns:
            Path: The path to the first file in the rawfiles list.

        Raises:
            StructuredError: If the input files are not consistent or if the
            list is empty.

        """
        self._is_correct_inputfiles(rawfiles)
        rawfile: Path = rawfiles[0]
        return rawfile

    def _is_correct_inputfiles(self, rawfiles: tuple[Path, ...]) -> bool:
        """Check if the input files are consistent.

        Args:
            rawfiles (tuple[Path, ...]): A tuple of paths to the raw files.
            Must be non-empty and contain only files with allowable extensions.

        Returns:
            bool: True if the input files are consistent, False otherwise.

        Raises:
            StructuredError: If there is an error in the input files or if the
            list is empty.

        """
        mask = self.READABLE_EXTENSIONS
        suffixes = [p.suffix for p in rawfiles]
        c = collections.Counter(suffixes)
        cnt = sum(v for k, v in c.items() if k in mask)
        if cnt > 1:
            error_message = "Too many data files."
        elif cnt < 1:
            error_message = (
                "Missing data file. "
                "Only files with the following extensions are allowd: "
                f"{' '.join(mask)}"
            )
        else:
            return True
        raise StructuredError(error_message, 1)
