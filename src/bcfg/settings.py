from pathlib import Path

# Folder must exist. An absolute path to your download directory
DOWNLOAD_PATH = Path(r".")

# Use "chrome", "chromium", "firefox", "opera", "ie", "edge"
# I recommend using the most updated version official google chrome or chromium.
# Other browsers are not really tested.
# If one does not work try another. Updating your browser may help.
BROWSER = "chrome"

# You only need one path to the binary (the executable file) named in the option BROWSER
# Try the command
#       which google-chrome
# or whatever your command is for the browser (chromium-browser, firefox, etc)
# That path goes here. You can also find paths by right clicking and looking in properties of icons
# HINT: This probably won't be your path.
CHROME_BINARY = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")
FIREFOX_BINARY = ""
CHROMIUM_BINARY = ""
EDGE_BINARY = ""
IE_BINARY = ""
OPERA_BINARY = ""

# The path to a txt file where you will list bandcamp album urls to batch download.
ALBUM_LINKS_TXT = Path(r"C:\Users\x\PycharmProjects\bandcamp-flac-get\album_links.txt")

# Select one: Format options are "mp3" "mp3-vo" "mp3-320" "flac" "vorbis"
FORMAT = "mp3"

# When bandcamp can't respond fast enough, how long should the browser wait before giving up?
# You can change this if you want.
TIMEOUT_TIME = 1000000000

# When you're done write out (CTRL+O) and exit (CTRL+X)
