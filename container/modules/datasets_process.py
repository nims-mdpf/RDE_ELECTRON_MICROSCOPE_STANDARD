from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from rdetoolkit.errors import catch_exception_with_message
from rdetoolkit.models.rde2types import RdeInputDirPaths, RdeOutputResourcePath
from rdetoolkit.rde2util import Meta

from modules.modules_em.factory import EmFactory
from modules.modules_temdm3.factory import TemDm3Factory


def temdm3_module(
    srcpaths: RdeInputDirPaths,
    resource_paths: RdeOutputResourcePath,
) -> None:
    """Process TEM-DM3 module for the RDE task.

    This function performs the following actions:
    1. Retrieves the TEM-DM3 class to use based on the configuration file.
    2. Checks consistency of input file.
    3. Gets the class to be used for each measurement method.
    4. Reads input files and saves raw-metadata as a CSV file.
    5. Saves metadata.json file.
    6. Visualizes measurement data if necessary.
    7. Overwrites invoice.json file with default values.
    8. Overwrites invoice.json file with measurement method.
    9. Overwrites invoice.json file with measured date/time.

    Args:
        srcpaths (RdeInputDirPaths): The source paths for the RDE task support directory and resource directories.
        resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

    Returns:
        None

    Raises:
        ValueError: If an error occurs during any of the above actions.

    """
    # -- Get the class to use --
    module = TemDm3Factory.get_base_objects()

    # -- Checking consistensy of input file --
    rawfile = module.file_reader.check_for_consistency(resource_paths.rawfiles)

    # -- Get the class to be used for each method --
    metadata_def, default_value, measurement_method = module.assign_objects_by_method(
        rawfile,
        srcpaths.tasksupport,
    )

    # -- Read input file --
    _, original_metadata = module.spectral_analizer.parse()

    # -- Save raw-metadata as csv --
    module.structured_processor.save_csv(
        original_metadata,
        resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_metadata.csv"),
    )

    # -- Save metadata.json
    meta: dict[str, Any] = {}
    for key, value in zip(original_metadata['key'], original_metadata['value']):
        meta[key] = value
    module.meta_parser.parse(meta, metadata_def)
    module.meta_parser.save_meta(
        resource_paths.meta.joinpath("metadata.json"),
        Meta(metadata_def),
    )

    # -- Visualize measurement data --
    module.spectral_analizer.visualize(resource_paths)

    # -- Overwrite invoice.json
    module.invoice_writer.overwrite_invoice_default_csv(
        resource_paths,
        default_value,
    )
    module.invoice_writer.overwrite_invoice_measurement_method(
        resource_paths,
        measurement_method,
    )
    operation_date_time = module.meta_parser.get_operation_datetime(meta)
    if operation_date_time is not None:
        module.invoice_writer.overwrite_invoice_measurement_measured_date(
            resource_paths,
            operation_date_time,
        )


def em_module(
    srcpaths: RdeInputDirPaths,
    resource_paths: RdeOutputResourcePath,
) -> None:
    """Process input data, visualizes measurement data, and save structured data.

    This function performs the following actions:
    1. Retrieves the class to use based on the configuration file.
    2. Reads input files and saves raw-metadata as a CSV file.
    3. Visualizes measurement data if necessary.
    4. Saves metadata.json file.

    Args:
        srcpaths (RdeInputDirPaths): The source paths for the RDE task support directory and resource directories.
        resource_paths (RdeOutputResourcePath): The output paths for the RDE resources.

    Returns:
        None

    Raises:
        ValueError: If an error occurs during any of the above actions.

    """
    # -- Get the class to use --
    metadata_def, module = EmFactory.get_objects(resource_paths.rawfiles[0], srcpaths.tasksupport)

    # -- Read input file --
    _, original_metadata = module.spectral_analizer.parse()

    # -- Save raw-metadata as csv --
    module.structured_processor.save_csv(
        original_metadata,
        resource_paths.struct.joinpath(f"{resource_paths.rawfiles[0].stem}_metadata.csv"),
    )

    # -- Visualize measurement data if necessary --
    module.spectral_analizer.visualize(resource_paths)

    # -- Save metadata.json --
    meta: dict[str, Any] = {}
    for key, value in zip(original_metadata['key'], original_metadata['value']):
        meta[key] = value
    module.meta_parser.parse(meta, metadata_def)

    new_dict: dict[str, Any] = {}
    dt = datetime.fromtimestamp(
        resource_paths.rawfiles[0].stat().st_ctime,
        tz=timezone.utc,
    )
    new_dict['file_last_modified_date_time'] = dt.strftime('%Y/%m/%d %H:%M:%S')
    module.meta_parser.const_meta_info.update(new_dict)

    module.meta_parser.save_meta(
        resource_paths.meta.joinpath("metadata.json"),
        Meta(metadata_def),
    )


@catch_exception_with_message(
    error_message="ERROR: failed in data processing", error_code=50)
def dataset(
    srcpaths: RdeInputDirPaths,
    resource_paths: RdeOutputResourcePath,
) -> None:
    """Run the data processing pipeline given the input and output directory paths.

    This function parses the configuration file at the specified path, validates
    its content, and determines which module to run based on the 'tem_dm3_mode'
    flag. If TEM-DM3 mode is enabled, it runs the temdm3_module function; otherwise,
    it falls back to default_module.

    Args:
        srcpaths (RdeInputDirPaths): The input directory paths.
        resource_paths (RdeOutputResourcePath): The output directory paths for resources.

    Returns:
        None

    """
    try:
        mode = hasattr(srcpaths.config, "custom") and srcpaths.config.custom.get("tem_dm3_mode", False)
    except AttributeError:
        # If 'custom' is present but 'tem_dm3_mode' is not
        return em_module(srcpaths, resource_paths)
    if mode:
        return temdm3_module(srcpaths, resource_paths)
    return em_module(srcpaths, resource_paths)
