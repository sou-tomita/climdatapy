#! /usr/bin/env python3

from pathlib import Path
import logging
import subprocess


CERES_URL = (
    "https://data.asdc.earthdata.nasa.gov/"
    "asdc-prod-protected/CERES/CERES_EBAF_Edition4.1/"
    "CERES_EBAF_Edition4.1_200003-202203.nc"
)

CERES_FILENAME = "CERES_EBAF_Edition4.1_200003-202203.nc"


def get_url() -> str:
    return CERES_URL


def get_save_fpath(data_dir: Path) -> Path:
    return data_dir / CERES_FILENAME


def ceres_download(
    data_dir: Path,
    exist_skip: bool = False,
) -> None:

    url = get_url()
    save_fpath = get_save_fpath(data_dir)

    save_fpath.parent.mkdir(parents=True, exist_ok=True)

    if exist_skip and save_fpath.exists():
        logging.info(f"Skip existing file: {save_fpath}")
        return

    cookie_file = Path.home() / ".urs_cookies"
    netrc_file = Path.home() / ".netrc"

    if not cookie_file.exists():
        raise FileNotFoundError(
            f"Earthdata cookie file not found: {cookie_file}"
        )

    if not netrc_file.exists():
        raise FileNotFoundError(
            f"Earthdata netrc file not found: {netrc_file}"
        )

    command = [
        "curl",
        "-f",
        "-b", str(cookie_file),
        "-c", str(cookie_file),
        "-L",
        "-n",
        "--retry", "3",
        "-o", str(save_fpath),
        url,
    ]

    logging.info(f"Downloading {url}")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError:
        save_fpath.unlink(missing_ok=True)
        raise

    logging.info(f"{url} ==> {save_fpath}")