 
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType
from pathlib import Path
import os
import wget
from fake_useragent import UserAgent
import sys
from dotenv import load_dotenv

load_dotenv()

# CONFIG
CHROME_BINARY = os.environ["CHROME_BINARY"]
DOWNLOAD_PATH = Path(os.environ["DOWNLOAD_PATH"])
if not DOWNLOAD_PATH.exists():
    sys.exit()
ALBUM_LINKS_TXT = Path('./album_links.txt')
TIMEOUT_TIME = 1000000000

# CONSTANTS
XPATH_FREE_DOWNLOAD = '//*[@id="trackInfoInner"]/ul/li[1]/div/h4/button'
XPATH_NAME_PRICE_INPUT = '//*[@id="userPrice"]'
XPATH_PRICE_LABEL = '//*[@id="fan_email"]/div[1]/div[1]/div[1]/span/span[2]/span'
XPATH_NAME_PRICE_DOWNLOAD_SHOW = '//*[@id="fan_email"]/div[2]/div[6]/div/a'
XPATH_NAME_PRICE_DOWNLOAD = '//*[@id="downloadButtons_download"]/div/button'
XPATH_FORMAT_DROPDOWN = '//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[3]/span'
XPATH_FLAC_SELECT = '//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[4]/ul/li[3]/span[2]'
XPATH_DOWNLOAD_ANCHOR = '//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/span/a'
XPATH_ERROR_PREPARING = '//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[2]/div[3]/div[2]/a'

SKIP_SWITCH = False  # I wish I had a more elegant solution than this but fuck it.


def get_album_links_from_file(p=ALBUM_LINKS_TXT):
    return [line.strip() for line in p.read_text().split('\n') if 'bandcamp.com/album/' in line]


def get_driver(binary_location: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9225")
    options.add_argument("window-size=1400,600")
    options.add_argument(f"user-agent={UserAgent().random}")
    options.binary_location = binary_location
    options.add_experimental_option("detach", True)
    service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
    return webdriver.Chrome(service=service, options=options)


def get_element(w, xpath: str, elem_descrip: str):
    try:
        button = w.until(
            EC.element_to_be_clickable(
                (By.XPATH, xpath)
            )
        )
        return button
    except NoSuchElementException:
        print(f"Can't Find {elem_descrip} element")


def check_price(label):
    return True if "(no minimum)" in label.get_attribute('innerHTML').strip() else False


def get_download_link(w):
    if SKIP_SWITCH:
        return ''
    else:
        get_element(w, XPATH_FORMAT_DROPDOWN, "Format Dropdown Selection").click()
        get_element(w, XPATH_FLAC_SELECT, "FLAC option").click()

        # This successfully gets the link for the download
        return get_element(w, XPATH_DOWNLOAD_ANCHOR, "download anchor").get_attribute('href')


def handle_name_price(w):
    global SKIP_SWITCH
    get_element(w, XPATH_NAME_PRICE_INPUT, "Name Price Input").send_keys("0")
    if check_price(get_element(w, XPATH_PRICE_LABEL, "Price Label")):
        get_element(w, XPATH_NAME_PRICE_DOWNLOAD_SHOW, "Show Download Link for Name Price").click()
        get_element(w, XPATH_NAME_PRICE_DOWNLOAD, "Download Button for Name Price").click()
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
    print("Starting download.")
    os.chdir(DOWNLOAD_PATH)
    filename = wget.download(url)
    print(f"Downloaded {filename}")


def get_albums():
    albums_to_get = get_album_links_from_file()
    with get_driver(CHROME_BINARY) as driver:
        download_urls = [get_album(driver, album, TIMEOUT_TIME) for album in albums_to_get]

    for download in download_urls:
        print(download)
        if not download == '':
            download_zip_file(download)

