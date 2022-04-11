from pathlib import Path

# Folder must exist. An absolute path to your download directory
# Leave the r that is before the quotes like r"" -- it's supposed to be there.
DOWNLOAD_PATH = r"./zips"

# Use "chrome", "chromium", "firefox", "opera", "ie", "edge"
# I recommend using the most updated version official google chrome or chromium.
# Other browsers are not really tested.
# If one does not work try another. Updating your browser may help.
BROWSER = r"chrome"

# You only need one path to the binary (the executable file) named in the option BROWSER
# Try the command
#       which google-chrome
# or whatever your command is for the browser (chromium-browser, firefox, etc)
# That path goes here. You can also find paths by right clicking and looking in properties of icons
# HINT: This probably won't be your path.
CHROME_BINARY = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CHROMIUM_BINARY = r""

# The path to a txt file where you will list bandcamp album urls to batch download.
ALBUM_LINKS_TXT = r"./album_links.txt"

# Select one: Format options are "mp3" "mp3-vo" "mp3-320" "flac" "vorbis"
FORMAT = r"mp3"

# When bandcamp can't respond fast enough, how long should the browser wait before giving up?
# You can change this if you want.
TIMEOUT_TIME = 1000000000

# When you're done write out (CTRL+O) and exit (CTRL+X)

# Don't touch these
DOWNLOAD_PATH = Path(DOWNLOAD_PATH)
CHROME_BINARY = Path(CHROME_BINARY)
CHROMIUM_BINARY = Path(CHROMIUM_BINARY)
ALBUM_LINKS_TXT = Path(ALBUM_LINKS_TXT)
