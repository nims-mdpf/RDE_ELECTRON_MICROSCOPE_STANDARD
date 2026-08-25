import os
import shutil
from typing import Union

# import pytest


def setup_inputdata_folder(inputdata_name: Union[str, list[str]]):
    """テスト用でdataフォルダ群の作成とrawファイルの準備

    Args:
        inputdata_name (Union[str, list[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "inputdata"), exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    tasksupport_original_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        "templates",
        "template",
        "tasksupport",
    )

    if isinstance(inputdata_name, list):
        for item in inputdata_name:
            shutil.copy(
                os.path.join(inputdata_original_path, item),
                os.path.join(destination_path, "inputdata"),
            )
    else:
        shutil.copy(
            os.path.join(inputdata_original_path, inputdata_name),
            os.path.join(destination_path, "inputdata"),
        )
    if not os.path.exists(os.path.join(destination_path, "tasksupport")):
        shutil.copytree(tasksupport_original_path, os.path.join(destination_path, "tasksupport"))


def setup_invoice_file(path: str):
    """テスト用でinvoiceファイルの準備

    Args:
        path (Union[str, list[str]]): rawファイル名
    """
    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, "invoice"), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    shutil.copy(
        os.path.join(inputdata_original_path, path),
        os.path.join(destination_path, "invoice"),
    )


def setup_file(dirname: str, path: str):
    """Sets up the file structure and copies a specified file to a destination directory.
    This function creates a directory structure under a "data" directory located two levels up from the current file's directory.
    It then copies a file from an "inputdata" directory located three levels up from the current file's directory to the newly created directory.

    Args:
        dirname (str): The name of the subdirectory to create under the "data" directory.
        path (str): The relative path of the file to copy from the "inputdata" directory.

    Raises:
        OSError: If the file or directory operations fail.

    """

    destination_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    os.makedirs(destination_path, exist_ok=True)
    os.makedirs(os.path.join(destination_path, dirname), exist_ok=True)
    inputdata_original_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "inputdata")

    shutil.copy(
        os.path.join(inputdata_original_path, path),
        os.path.join(destination_path, dirname),
    )


class TestOutputCase1:
    """case1
    <pattern1>の入出力テスト
    入力ファイル: xxxxを参照
    """

    # inputdata: Union[str, list[str]] = "<テストで使用する入力ファイルパス: リポジトリ直下inputdataディィレクトリ以下>"
    # invoice: str = "<テストで使用するinvoice.jsonパス: リポジトリ直下inputdataディィレクトリ以下>"
    inputdata: Union[str, list[str]] = "test1/inputdata/sample-data.txt"
    invoice: str = "test1/invoice/invoice.json"

    def test_setup(self):
        # setup_inputdata_folder(self.inputdata)
        # setup_invoice_file(self.invoice)
        ...

    def test_raw_data(self, setup_main, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "raw", raw_data))
        ...

    def test_main_image(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "main_image", img_name))
        ...

    def test_structured(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "structured", csv_name))
        ...

    def test_thumbnail(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "thumbnail", "sample-data.png"))
        ...

    def test_metadata(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))
        ...


class TestOutputCase2:
    """case2
    <pattern2>の入出力テスト
    入力ファイル: xxxxを参照
    """

    # inputdata: Union[str, list[str]] = "<テストで使用する入力ファイルパス:リポジトリ直下inputdataディィレクトリ以下>"
    # invoice: str = "<テストで使用するinvoice.jsonパス>"
    inputdata: Union[str, list[str]] = "test1/inputdata/sample-data.txt"
    invoice: str = "test1/invoice/invoice.json"

    def test_setup(self):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # setup_inputdata_folder(self.inputdata)
        # setup_invoice_file(self.invoice)
        ...

    def test_raw_data(self, setup_main, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "raw", "<テスト対象のファイルパス>"))
        ...

    def test_main_image(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "main_image", "<テスト対象のファイルパス>"))
        ...

    def test_structured(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "structured", "<テスト対象のファイルパス>"))
        ...

    def test_thumbnail(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "thumbnail", "<テスト対象のファイルパス>"))
        ...

    def test_metadata(self, data_path):
        # 使用時は以下のコメントアウトを外し、このコメンを削除
        # assert os.path.exists(os.path.join(data_path, "meta", "metadata.json"))
        ...
