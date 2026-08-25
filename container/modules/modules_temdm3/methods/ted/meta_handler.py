from __future__ import annotations

from modules.modules_temdm3.meta_handler import MetaParser as TemDm3MetaParser


class MetaParser(TemDm3MetaParser):
    """Class for parsing and saving metadata.

    This class is for parsing pre-acquired metadata and saving it to a file.
    It only handles constant metadata and does not support repeated metadata.

    Attributes:
        prefix_meta (str): Prefix of the item title of the json data.

    """

    PREFIX_META = 'ted'

    def __init__(self) -> None:
        super().__init__()
        self.prefix_meta = self.PREFIX_META
