"""Download pinned public workbooks used by the macro data-gate audits."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import requests


SOURCES = {
    "SPFmicrodata.xlsx": (
        "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/"
        "survey-of-professional-forecasters/historical-data/SPFmicrodata.xlsx?"
        "hash=FC620719B822510E215BA3908F0E3681&sc_lang=en",
        "d45af2eaebe11e8c7a0635d3f868d5d85897e5bc5cc3d8cb477c243b31faa076",
    ),
    "ROUTPUTQvQd.xlsx": (
        "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/"
        "real-time-data/data-files/xlsx/ROUTPUTQvQd.xlsx?"
        "hash=34FA1C6BF0007996E1885C8C32E3BEF9&sc_lang=en",
        "bf0c4c1b6b902283bfb94fe7b7d94e003ff68fb926aebb0169504bbe213a055c",
    ),
    "cpiQvMd.xlsx": (
        "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/"
        "real-time-data/data-files/xlsx/cpiQvMd.xlsx?"
        "hash=9659566E92130D1A394C7FEDB6EC4115&sc_lang=en",
        "57d28f99b28ca9a37801fcdd5026fae9b859e58b0f3dc1e150a55c544598bc34",
    ),
    "rucQvMd.xlsx": (
        "https://www.philadelphiafed.org/-/media/FRBP/Assets/Surveys-And-Data/"
        "real-time-data/data-files/xlsx/rucQvMd.xlsx?"
        "hash=A96BC0C2253B04EAEB8C4DC42D4F5CBA&sc_lang=en",
        "d971e59d3ed5f1322a46631743508fb1ad5eee39bfbe12425a641a277fdd9b9a",
    ),
}


def download(output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, (url, expected) in SOURCES.items():
        destination = output_dir / filename
        if destination.exists():
            actual = hashlib.sha256(destination.read_bytes()).hexdigest()
            if actual != expected:
                raise ValueError(f"existing file has unexpected hash: {destination}")
            print(f"verified {destination} {actual}")
            continue
        response = requests.get(url, timeout=120)
        response.raise_for_status()
        actual = hashlib.sha256(response.content).hexdigest()
        if actual != expected:
            raise ValueError(f"downloaded hash mismatch for {filename}: {actual}")
        destination.write_bytes(response.content)
        print(f"downloaded {destination} {actual}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    download(args.output_dir)


if __name__ == "__main__":
    main()
