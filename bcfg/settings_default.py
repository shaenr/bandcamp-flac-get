from pathlib import Path

PROJECT_PATH = Path(r"..\..\..\bandcamp-flac-get").resolve()
# Folder must exist. An absolute path to your download directory
DOWNLOAD_PATH = PROJECT_PATH / "zips"

# Use "chrome", "chromium"
BROWSER = "chrome"

# You only need one path to the binary (the executable file) named in the option BROWSER
# Try the command
#       which google-chrome
# or whatever your command is for the browser (chromium-browser, firefox, etc)
# That path goes here. You can also find paths by right clicking and looking in properties of icons
# HINT: This probably won't be your path.
CHROME_BINARY = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROMIUM_BINARY = r"/usr/bin/chromium-browser"

# The path to a txt file where you will list bandcamp album urls to batch download.
ALBUM_LINKS_TXT = PROJECT_PATH / "album_links.txt"

# Select one: Format options are "mp3" "mp3-vo" "mp3-320" "flac" "vorbis"
FORMAT = "mp3"
TIMEOUT_TIME = 1000000000

DOWNLOAD_PATH = Path(DOWNLOAD_PATH).resolve()
CHROME_BINARY = Path(CHROME_BINARY).resolve()
CHROMIUM_BINARY = Path(CHROMIUM_BINARY).resolve()
ALBUM_LINKS_TXT = Path(ALBUM_LINKS_TXT).resolve()
