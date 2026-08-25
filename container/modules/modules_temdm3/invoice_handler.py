from __future__ import annotations

from pathlib import Path
from typing import Any

from rdetoolkit.invoicefile import InvoiceFile, overwrite_invoicefile_for_dpfterm
from rdetoolkit.models.rde2types import RdeOutputResourcePath
from rdetoolkit.rde2util import get_default_values, read_from_json_file


class InvoiceWriter:
    """Invoice overwriter.

    Overwrite invoice.json files depending on conditions.

    """

    def overwrite_invoice_default_csv(
        self,
        resource_paths: RdeOutputResourcePath,
        default_value: Path,
    ) -> None:
        """Overwrite the values of an invoice file with the default value.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.
            default_value (Path): The path to the default_value csv file.

        Returns:
            None

        """
        invoice_info = get_default_values(default_value)
        self._overwrite_invoicefile(resource_paths, invoice_info)

    def overwrite_invoice_measurement_method(
        self,
        resource_paths: RdeOutputResourcePath,
        measurement_method: str,
    ) -> None:
        """Overwrite the measurement method of an invoice file with the given string.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.
            measurement_method (str): The new measurement method for the
            invoice file. Must be a non-empty string.

        Returns:
            None

        Raises:
            ValueError: If the provided measurement method is empty or not a string.

        """
        invoice_info: dict[str, Any] = {}
        invoice_info["common_data_type"] = measurement_method
        self._overwrite_invoicefile(resource_paths, invoice_info)

    def overwrite_invoice_measurement_measured_date(
        self,
        resource_paths: RdeOutputResourcePath,
        measurement_measured_date: str,
    ) -> None:
        """Overwrite the measurement measured date of an invoice file with the given string.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.
            measurement_measured_date (str): The new measurement measured date
            for the invoice file. Must be a non-empty string.

        Returns:
            None

        Raises:
            ValueError: If the provided measurement measured date is empty or
            not a string.

        """
        if not self._is_entry_measurement_measured_data(resource_paths):
            return
        invoice_info: dict[str, Any] = {}
        invoice_info["measurement_measured_date"] = measurement_measured_date
        self._overwrite_invoicefile(resource_paths, invoice_info)

    def _is_entry_measurement_measured_data(
        self,
        resource_paths: RdeOutputResourcePath,
    ) -> bool:
        invoice_obj = read_from_json_file(resource_paths.invoice_org)
        return invoice_obj.get('measurement_measured_date') is not None

    def _overwrite_invoicefile(
        self,
        resource_paths: RdeOutputResourcePath,
        new_values: dict[str, Any],
    ) -> None:
        """Overwrite the values of an invoice file with the given dictionary.

        Args:
            resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.
            new_values (dict[str, Any]): A dictionary containing the new values
            for the invoice file.

        Returns:
            None

        """
        invoice_obj = read_from_json_file(resource_paths.invoice_org)
        overwrite_invoicefile_for_dpfterm(
            invoice_obj,
            resource_paths.invoice_org,
            resource_paths.invoice_schema_json,
            new_values,
        )
        invoice_org_obj = InvoiceFile(resource_paths.invoice_org)
        invoice_org_obj.overwrite(resource_paths.invoice.joinpath("invoice.json"))
