# Folder must exist
DOWNLOAD_PATH = "/home/shaen/bandcamp-flac-get/zips"

# Use "chrome" "chromium" "firefox" "opera" "ie" "edge"
# I recommend using the most updated version official google chrome or chromium.
# Other browsers are not really tested.
# If one does not work try another. Updating your browser may help.
BROWSER = "chrome"

# You only need the path to the binary named in the option BROWSER
CHROME_BINARY = "/usr/bin/google-chrome"
CHROMIUM_BINARY = "/snap/bin/chromium"
FIREFOX_BINARY = "/usr/bin/firefox"
EDGE_BINARY = ""
IE_BINARY = ""
OPERA_BINARY = ""

# The text file of bandcamp album links to batch download
ALBUM_LINKS_TXT = "/home/shaen/bandcamp-flac-get/album_links.txt"

# Format options are "mp3" "mp3-vo" "mp3-320" "flac" "vorbis"
FORMAT = "mp3-vo"

# When bandcamp can't respond fast enough, how long should the browser wait before giving up?
TIMEOUT_TIME = 1000000000