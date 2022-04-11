from . import settings
# if settings.DEBUG:
#     from . import settings_example as settings
from argparse import Namespace
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as CService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager as CDriverManager
from webdriver_manager.utils import ChromeType
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pathlib import Path
import os
import wget
from fake_useragent import UserAgent
import sys
from .xpaths import *
import typing

# CONFIG IMPORT
BROWSER = settings.BROWSER
DOWNLOAD_PATH = Path(settings.DOWNLOAD_PATH)
ALBUM_LINKS_TXT = Path(settings.ALBUM_LINKS_TXT)
TIMEOUT_TIME = settings.TIMEOUT_TIME
SKIP_SWITCH = False  # I wish I had a more elegant solution than this but fuck it.


def sanity_check():
    return sys.exit(1) if not DOWNLOAD_PATH.exists() else True


def get_album_links_from_file(p=ALBUM_LINKS_TXT):
    return [
        line.strip()
        for line in p.read_text().split("\n")
        if "bandcamp.com/album/" in line
    ]


def _get_chrome_options(binary_location: str):
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--test-type")
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9225")
    options.add_argument("window-size=1400,600")
    options.add_argument(f"user-agent={UserAgent().chrome}")
    options.binary_location = binary_location
    options.add_experimental_option("detach", True)
    return options


# def _get_opera_options(binary_location: str):
#     options = webdriver.ChromeOptions()
#     options.add_argument('allow-elevated-browser')
#     options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
#     return options


def _get_driver(driver, v3, v4service=None, opts=None, variation=None):
    options = opts if opts is not None else None
    service = v4service if v4service is not None else None
    try:
        if variation == "firefox":
            driver(executable_path=v3)
        elif variation == "opera":
            driver(executable_path=v3, options=options)
    except Exception as exc:
        print(exc)
        driver(v3, options=options)
    return driver(v3)


def get_driver(binary_location: str, browser: typing.Union[str, None]):
    if browser == "chromium":
        return _get_driver(
            driver=webdriver.Chrome,
            v3=CDriverManager(chrome_type=ChromeType.CHROMIUM).install(),
            v4service=CService(
                CDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            ),
            opts=_get_chrome_options(binary_location),
        )
    elif browser == "chrome":
        return _get_driver(
            driver=webdriver.Chrome,
            v3=CDriverManager().install(),
            v4service=CService(CDriverManager().install()),
            opts=_get_chrome_options(binary_location),
        )
    elif browser == "firefox":
        return _get_driver(
            driver=webdriver.Firefox,
            v3=GeckoDriverManager().install(),
            v4service=FirefoxService(GeckoDriverManager().install()),
            variation="firefox",
        )
    elif browser == "ie":
        return _get_driver(
            driver=webdriver.Ie,
            v3=IEDriverManager().install(),
            v4service=IEService(IEDriverManager().install()),
        )
    elif browser == "edge":
        return _get_driver(
            driver=webdriver.Edge,
            v3=EdgeChromiumDriverManager().install(),
            v4service=EdgeService(EdgeChromiumDriverManager().install()),
            opts=_get_chrome_options(binary_location),
        )
    elif browser == "opera":
        return _get_driver(
            driver=webdriver.Opera,
            v3=OperaDriverManager().install(),
            variation="opera",
            opts=_get_chrome_options(),
        )


def get_element(w, xpath: str, elem_descrip: str):
    try:
        button = w.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        return button
    except NoSuchElementException:
        print(f"Can't Find {elem_descrip} element")


def check_price(label):
    return True if "(no minimum)" in label.get_attribute("innerHTML").strip() else False


def get_format_xpath_from_settings_option():
    file_format = settings.FORMAT
    if file_format == "mp3" or file_format == "mp3-vo":
        return XPATH_MP3_VO_SELECT
    elif file_format == "mp3-320":
        return XPATH_MP3_320_SELECT
    elif file_format == "flac":
        return XPATH_FLAC_SELECT
    elif file_format == "vorbis":
        return XPATH_VORBIS_SELECT
    else:
        return XPATH_MP3_VO_SELECT


def get_download_link(w):
    if SKIP_SWITCH:
        return ""
    else:
        get_element(w, XPATH_FORMAT_DROPDOWN, "Format Dropdown Selection").click()
        get_element(w, get_format_xpath_from_settings_option(), "format option").click()

        # This successfully gets the link for the download
        return get_element(w, XPATH_DOWNLOAD_ANCHOR, "download anchor").get_attribute(
            "href"
        )


def handle_name_price(w):
    global SKIP_SWITCH
    get_element(w, XPATH_NAME_PRICE_INPUT, "Name Price Input").send_keys("0")
    if check_price(get_element(w, XPATH_PRICE_LABEL, "Price Label")):
        get_element(
            w, XPATH_NAME_PRICE_DOWNLOAD_SHOW, "Show Download Link for Name Price"
        ).click()
        get_element(
            w, XPATH_NAME_PRICE_DOWNLOAD, "Download Button for Name Price"
        ).click()
    else:
        SKIP_SWITCH = True


def get_album(d, album_url, wait_time):
    global SKIP_SWITCH
    SKIP_SWITCH = False
    wait = WebDriverWait(d, wait_time)
    d.get(album_url)

    get_element(wait, XPATH_FREE_DOWNLOAD, "Free Download Link").click()
    if "bandcamp.com/download?id=" not in d.current_url:
        handle_name_price(wait)
    return get_download_link(wait)


def download_zip_file(url):
    print(f"Starting download. Getting file format: {settings.FORMAT}")
    os.chdir(DOWNLOAD_PATH)
    filename = wget.download(url)
    print(f"Downloaded {filename}")


def get_binary_from_browser_option():
    browser = settings.BROWSER
    if browser == "chrome":
        return settings.CHROME_BINARY
    if browser == "chromium":
        return settings.CHROMIUM_BINARY
    if browser == "firefox":
        return settings.FIREFOX_BINARY
    if browser == "opera":
        return settings.OPERA_BINARY
    if browser == "ie":
        return settings.IE_BINARY
    if browser == "edge":
        return settings.EDGE_BINARY


def get_albums():
    albums_to_get = get_album_links_from_file()
    with get_driver(get_binary_from_browser_option(), BROWSER) as driver:
        download_urls = [
            get_album(driver, album, TIMEOUT_TIME) for album in albums_to_get
        ]

    for download in download_urls:
        print(download)
        if not download == "":
            download_zip_file(download)


def bcfg_cli(argv: Namespace):
    if not len(sys.argv) > 1:
        pass
    if argv.gui:
        from bcfg.gui import configdialog as GUI
        GUI.GUI()
        sys.exit()
    if argv.chrome:
        settings.BROWSER = "chrome"
        settings.CHROME_BINARY = Path(argv.chrome)
    if argv.chromium:
        settings.BROWSER = "chromium"
        settings.CHROMIUM_BINARY = Path(argv.chromium)

    settings.TIMEOUT_TIME = argv.timeout if argv.timeout else settings.TIMEOUT_TIME
    settings.ALBUM_LINKS_TXT = argv.input if argv.input else settings.ALBUM_LINKS_TXT
    settings.FORMAT = argv.format if argv.format else settings.FORMAT
    settings.DOWNLOAD_PATH = argv.output if argv.output else settings.DOWNLOAD_PATH

    sanity_check()

    try:
        get_albums()
    except IsADirectoryError as exc:
        print("You need to open this file and configure paths and options before you run the program:")
        print(Path("src/bcfg/settings.py").resolve())


if __name__ == "__main__":
    bcfg_cli()