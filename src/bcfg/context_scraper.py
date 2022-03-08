import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from sys import argv, exit
from lxml import etree
from pathlib import Path
import json

script, *args = argv

XP_ARTIST_NAME = '//*[@id="band-name-location"]/span[1]'
XP_LOCATION = '//*[@id="band-name-location"]/span[2]'
XP_ARTIST_BIO_TEXT = '//*[@id="bio-text"]'
XP_ARTIST_AVATAR = '//*[@id="bio-container"]/div[1]/div/a/img'
XP_ALBUM_NAME = '//*[@id="name-section"]/h2'
XP_DATE_UPLOADED = '//*[@id="trackInfoInner"]/div[2]/text()'
XP_LICENSE = '//*[@id="license"]'

XP_TRACK_TABLE = '//*[@id="track_table"]'
XP_FIRST_TRACK_NAME = '//*[@id="track_table"]/tbody/tr[1]/td[3]/div/a/span'
XP_FIRST_TRACK_TIME = '//*[@id="track_table"]/tbody/tr[1]/td[3]/div/span'


def simple_parse_url(args):
    """
    This will discard all the args except the first one if there is any at all. If not it will exit.
    :param args: Needs at least one to be a url.
    :return:
    """
    if len(args) > 0 and "bandcamp.com/" in args[0]:
        return args[0]
    else:
        print("Are you sure that you passed a bandcamp url to the script as arg?")
        print(args)
        exit(1)


def get_headers():
    return {
        "User-Agent": UserAgent().random,
        "Accept-Language": "en-gb",
        "Accept-Encoding": "br,gzip,deflate",
        "Accept": "test/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Referer": "http://www.google.com",
    }


def get_response(url: str):
    headers = get_headers()
    html = requests.get(url, headers=headers)
    html.raise_for_status()
    return html


def init_soup(parser: str = "html.parser"):
    page = get_response(simple_parse_url(args))
    return BeautifulSoup(page.content, parser)


soup = init_soup()
dom = etree.HTML(str(soup))

# These were all very easy.
data = {
    "ARTIST": dom.xpath(XP_ARTIST_NAME)[0].text,
    "LOCATION": dom.xpath(XP_LOCATION)[0].text,
    "ARTIST_BIO_TEXT": dom.xpath(XP_ARTIST_BIO_TEXT)[0].text,
    "ARTIST_AVATAR": dom.xpath(XP_ARTIST_AVATAR)[0].get("src"),
    "ALBUM_NAME": dom.xpath(XP_ALBUM_NAME)[0].text,
    "DATE_UPLOADED": dom.xpath(XP_DATE_UPLOADED)[0],
    "LICENSE": dom.xpath(XP_LICENSE)[0].text,
}

data = {k: v.strip() for k, v in data.items()}

tracks = soup.find_all("span", {"class": "track-title"})
times = soup.find_all("span", {"class": ["time", "secondaryText"]})

for i, t in enumerate(times):
    time = t.text.strip()
    if ":" not in time:
        times.remove(t)

trackList = [
    (track.text.strip(), time.text.strip()) for track, time in zip(tracks, times)
]


trackData = {"tracks": []}

for track, time in trackList:
    trackEntry = {"track": track, "time": time}
    trackData["tracks"].append(trackEntry)

data["tracks"] = trackData


def serialize_json_file(data: dict, path_obj: Path, mode: str = "w"):
    with path_obj.open(mode) as write_obj:
        json.dump(data, write_obj, indent=4)


def write_to_file(p, d):
    out_file = Path(p)
    with out_file.open("w") as fo:
        json.dump(d, fo)


base_dir = "/media/$USER/Home/zips"
write_to_file(f"{base_dir}/{data['ARTIST']}-{data['ALBUM_NAME']}.json", data)
