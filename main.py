from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from pathlib import Path
import os
import wget

# CONFIG
CHROME_BINARY = "/path/to/chrome"          # You will need to use the path to Chrome here.
DOWNLOAD_PATH = Path.home()
ALBUM_LINKS_TXT = Path('./album_links.txt')

# CONSTANTS
XPATH_FREE_DOWNLOAD = '//*[@id="trackInfoInner"]/ul/li[1]/div/h4/button'
XPATH_NAME_PRICE_INPUT = '//*[@id="userPrice"]'
XPATH_PRICE_LABEL = '//*[@id="fan_email"]/div[1]/div[1]/div[1]/span/span[2]/span'
XPATH_NAME_PRICE_DOWNLOAD_SHOW = '//*[@id="fan_email"]/div[2]/div[6]/div/a'
XPATH_NAME_PRICE_DOWNLOAD = '//*[@id="downloadButtons_download"]/div/button'
XPATH_FORMAT_DROPDOWN = '//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[3]/span'
XPATH_FLAC_SELECT = '//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/div[4]/ul/li[3]/span[2]'
XPATH_DOWNLOAD_ANCHOR = '//*[@id="post-checkout-info"]/div[1]/div[2]/div[4]/span/a'

SKIP_SWITCH = False  # I wish I had a more elegant solution than this but fuck it.


def get_album_links(p=ALBUM_LINKS_TXT):
    return [line.strip() for line in p.read_text().split('\n') if 'bandcamp.com/album/' in line]


def get_driver(binary_location: str):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--test-type')
    options.add_argument("--disable-notifications")
    options.add_argument("--remote-debugging-port=9225");
    options.binary_location = binary_location
    return webdriver.Chrome(options=options)


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


def click(btn):
    btn.click()


def enter_zero(inp):
    inp.send_keys("0")


def check_price(label):
    return True if "(no minimum)" in label.get_attribute('innerHTML').strip() else False


def get_download_link(w):
    if SKIP_SWITCH:
        return ''
    else:
        click(get_element(w, XPATH_FORMAT_DROPDOWN, "Format Dropdown Selection"))
        click(get_element(w, XPATH_FLAC_SELECT, "FLAC option"))

        # This successfully gets the link for the download
        return get_element(w, XPATH_DOWNLOAD_ANCHOR, "download anchor").get_attribute('href')


def handle_name_price(w):
    global SKIP_SWITCH
    enter_zero(get_element(w, XPATH_NAME_PRICE_INPUT, "Name Price Input"))
    if check_price(get_element(w, XPATH_PRICE_LABEL, "Price Label")):
        click(get_element(w, XPATH_NAME_PRICE_DOWNLOAD_SHOW, "Show Download Link for Name Price"))
        click(get_element(w, XPATH_NAME_PRICE_DOWNLOAD, "Download Button for Name Price"))
    else:
        SKIP_SWITCH = True


def get_album(d, album_url, wait_time):
    wait = WebDriverWait(d, wait_time)
    d.get(album_url)

    click(get_element(wait, XPATH_FREE_DOWNLOAD, "Free Download Link"))
    if "bandcamp.com/download?id=" not in d.current_url:
        handle_name_price(wait)
    return get_download_link(wait)


def download_zip_file(url):
    print("Starting download.")
    os.chdir(DOWNLOAD_PATH)
    filename = wget.download(url)
    print(f"Downloaded {filename}")


if __name__ == '__main__':
    albums_to_get = get_album_links()
    with get_driver(CHROME_BINARY) as driver:
        download_urls = [get_album(driver, album, 5) for album in albums_to_get]

    for download in download_urls:
        if not download == '':
            download_zip_file(download)

    print("Done!")
