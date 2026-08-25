from __future__ import annotations

from pathlib import Path

from modules.modules_em.spectral_analyzer import SpectralAnalizer as EmSpectralAnalizer


class SpectralAnalizer(EmSpectralAnalizer):
    """Template class for analysing electron microscopy data files in Digital Microscope format."""

    def __init__(self, file_path: Path) -> None:
        super().__init__(file_path)
