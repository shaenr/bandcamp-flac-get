import sys
from argparse import (
    Namespace,
    FileType,
    ArgumentParser,
    RawDescriptionHelpFormatter
)
from bcfg import settings


def get_argv():
    parser = ArgumentParser(
        prog="bandcamp-flac-get/src/main.py",
        description="Generate flac/mp3/vorbis download links for bandcamp albums that are free (or name your own" 
        "price with no minimum price). It will download a zip with cover image, metadata, and files organized into "
        "folders.",
        formatter_class=RawDescriptionHelpFormatter
    )

    parser.add_argument('input',
                        type=FileType('r'),
                        default=settings.ALBUM_LINKS_TXT,
                        help="Read this txt file for bandcamp album links...")

    # verbosity_group = parser.add_mutually_exclusive_group(required=False)
    # verbosity_group.add_argument("-v", "--verbose", default=2, action="count",
    #                              help="increase logging level.")
    # verbosity_group.add_argument("-q", "--quiet", default=1, action="count",
    #                              help="decrease logging level.")

    browser_group = parser.add_mutually_exclusive_group(required=True)
    browser_group.add_argument("--chrome", default=settings.CHROME_BINARY,
                               help="Specify Chrome Binary")
    browser_group.add_argument("--chromium", default=settings.CHROMIUM_BINARY,
                               help="Specify Chromium Binary")

    parser.add_argument("-f", "--format", default="flac",
                        help='specify alternate format: "mp3" "mp3-vo" "mp3-320" "flac" "vorbis"')

    parser.add_argument("-t", "--timeout", type=int, default=settings.TIMEOUT_TIME,
                        help="Specify a timeout time in seconds...")

    return parser.parse_args()

