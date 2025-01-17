import argparse
import logging
import re
from datetime import datetime
from pathlib import Path

import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

from odemis import model
from odemis.dataio import csv
from odemis.dataio import hdf5
from odemis.util.angleres import project_angular_spectrum_to_grid

logging.basicConfig(format="%(asctime)s  %(levelname)-7s %(module)-15s: %(message)s", force=True)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Search settings for background files (blank).
BACKGROUND_SEPARATORS = [" ", "_", "-"]
BACKGROUND_SPECIFIERS = ["blank", "dark", "background"]


def locate_ar_spectrum_in_data(data):
    """
    The position of the AR spectrum data in the data list is not always the same.
    Use the metadata to locate it, which is a more robust way then directly indexing it.
    """
    for d in data:
        if d.metadata[model.MD_DESCRIPTION].lower() == "AR Spectrum".lower():
            return d


def format_data_for_projection(data):
    """
    Acquired data needs to be formatted to be accepted by `project_angular_spectrum_to_grid`.
    """
    data_squeezed = data.squeeze()
    if len(data_squeezed.shape) > 2:
        raise ValueError("Data contains more than one acquisition")
    return np.float64(data_squeezed.T)


def get_matching_background_file(fp):
    """
    Tries to find background file in same folder as measurement.
    See `BACKGROUND_SPECIFIERS` and `BACKGROUND_SEPARATORS` for configuration.

    Example
    -------
    If `sample_folder/measurement.h5` has a `sample_folder/measurement-blank.h5` in the same folder,
    it will be matched.

    Alternatively, if there is only one blank file in the folder, it will be matched:
    `sample_folder/measurement-1.h5`
    `sample_folder/measurement-2.h5`
    `sample_folder/measurement-3.h5`
    `sample_folder/blank.h5`  <-- Matched with any of the measurement files

    """
    background_file = None
    for sep in BACKGROUND_SEPARATORS:
        for spec in BACKGROUND_SPECIFIERS:
            potential_background_file = fp.with_stem(f"{fp.stem}{sep}{spec}")
            if potential_background_file.exists():
                background_file = potential_background_file

    if not background_file:
        # Check in folder for one background file for all
        potential_background_files = []
        for spec in BACKGROUND_SPECIFIERS:
            potential_background_files.extend(fp.parent.glob(f"*{spec}.h5"))

        if len(potential_background_files) == 1:
            background_file = potential_background_files.pop()
    return background_file


def process_raw_data(measurement, name, output_folder, background_measurement=None):
    """
    Takes raw measurement data and converts it to an angle corrected representation.
    Takes into a background measurement into account
    """
    if background_measurement is not None:
        measurement -= background_measurement
    measurement_formatted = format_data_for_projection(measurement)
    measurement_on_grid = project_angular_spectrum_to_grid(measurement_formatted)
    csv.export(output_folder / f"{name}.csv", measurement_on_grid)


def process_h5(fp, output_folder, background_fp=None):
    """
    Processes an h5 file, which consists of loading, handling repeated acquisition,
    correcting for background and storing the resulting csv.
    """
    acquisition_data = hdf5.read_data(fp)
    ar_data_raw = locate_ar_spectrum_in_data(acquisition_data)
    background_data_raw = None
    if background_fp:
        logger.info("Found matching blank file")
        background_data = hdf5.read_data(background_fp)
        background_data_raw = locate_ar_spectrum_in_data(background_data)

    if len(ar_data_raw.shape) == 5:
        if ar_data_raw.shape[-2:] == (1, 1):
            logger.info("Acquisition has single measurement point")
            process_raw_data(
                ar_data_raw,
                f"{Path(fp).stem}",
                output_folder=output_folder,
                background_measurement=background_data_raw
            )
        else:
            # ar_data_raw_indexed = np.moveaxis(ar_data_raw.reshape(*ar_data_raw.shape[:3], -1), -1, 0)
            logger.info(f"Acquisition has multiple measurement points")
            for idx in np.ndindex(ar_data_raw.shape[-2:]):
                ar_data_raw_sample = ar_data_raw[..., idx[0], idx[1]]
                process_raw_data(
                    ar_data_raw_sample,
                    f"{Path(fp).stem}-{idx[1]}-{idx[0]}",
                    output_folder=output_folder,
                    background_measurement=background_data_raw
                )
    else:
        raise ValueError("Acquisition not in expected format")


def path_type(arg):
    if arg is not None:
        path = Path(arg)
        if not path.exists():
            raise FileNotFoundError(f"{path} not found on the filesystem")
        return path


def main():
    parser = argparse.ArgumentParser(description='Converts EK h5 files to csv')
    parser.add_argument(
        '--path',
        type=path_type,
        help='Path of h5 file or folder containing h5 files. Folders can be nested. If none provided, spawn GUI to pick.'
    )
    args = parser.parse_args()

    if args.path is None:
        root = tk.Tk()
        root.withdraw()
        batch = messagebox.askquestion("Batch mode", "Process folder (yes) or single file (no)?")

        if batch == "yes":
            fp = Path(filedialog.askdirectory(title="Select EK measurement folder"))

        else:
            fp = Path(filedialog.askopenfilename(title="Select EK measurement file"))
    else:
        fp = args.path
    process_queue = []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if fp.is_dir():
        process_queue.extend(fp.glob("**/*.h5"))
        output_folder_parent = fp
    elif fp.is_file():
        process_queue.append(fp)
        output_folder_parent = fp.parent

    # Remove blank files
    process_queue = [
        f for f in process_queue
        if not re.search(
            rf"(?:[{''.join(BACKGROUND_SEPARATORS)}]|^)?({'|'.join(BACKGROUND_SPECIFIERS)})$", f.stem
        )
    ]
    # Walk through measurements, process them one by one
    output_folder = output_folder_parent / f"output-{timestamp}"
    for filename in process_queue:
        output_filename = output_folder / filename.relative_to(fp)
        # Make sure to recursively create the nested paths if present
        output_filename.parent.mkdir(parents=True, exist_ok=True)
        try:
            logger.info(f"Processing {filename}")
            process_h5(filename, output_filename.parent)
        except Exception as e:
            logger.error(e)
            continue

    return 0

if __name__ == "__main__":
    ret = main()
    exit(ret)
