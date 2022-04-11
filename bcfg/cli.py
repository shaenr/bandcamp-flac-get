import os.path
from argparse import (
    FileType,
    ArgumentParser,
    RawDescriptionHelpFormatter,
    ArgumentTypeError
)
from pathlib import Path
from bcfg import settings


def validate_output_dir(path):
    if os.path.isdir(path):
        return path
    else:
        raise ArgumentTypeError(
            f"output directory: {path} is not a valid directory path."
        )


def get_argv():
    parser = ArgumentParser(
        prog="bandcamp_flac_get.py",
        description="Generate flac/mp3/vorbis download links for bandcamp albums that are free (or name your own" 
        "price with no minimum price). It will download a zip with cover image, metadata, and files organized into "
        "folders.",
        formatter_class=RawDescriptionHelpFormatter
    )

    parser.add_argument("-i", "--input",
                        type=FileType('r'),
                        default=settings.ALBUM_LINKS_TXT,
                        help="Specify a txt as input file with bandcamp album links to download: one link per line...")

    parser.add_argument("-o", "--output",
                        type=validate_output_dir,
                        default=settings.DOWNLOAD_PATH,
                        help="Specify a directory in which to save the zip files scraped from bandcamp.")

    # verbosity_group = parser.add_mutually_exclusive_group(required=False)
    # verbosity_group.add_argument("-v", "--verbose", default=2, action="count",
    #                              help="increase logging level.")
    # verbosity_group.add_argument("-q", "--quiet", default=1, action="count",
    #                              help="decrease logging level.")

    browser_group = parser.add_mutually_exclusive_group(required=False)
    browser_group.add_argument("--chrome", default=settings.CHROME_BINARY,
                               help="Specify Chrome Binary")
    browser_group.add_argument("--chromium", default=settings.CHROMIUM_BINARY,
                               help="Specify Chromium Binary")

    parser.add_argument("-f", "--format", default="flac",
                        help='specify alternate format: "mp3" "mp3-vo" "mp3-320" "flac" "vorbis"')

    parser.add_argument("-t", "--timeout", type=int, default=settings.TIMEOUT_TIME,
                        help="Specify a timeout time in seconds...")

    parser.add_argument("-g", "--gui", action='store_true',
                        help="Open the GUI to configure default setting.")

    return parser.parse_args()

