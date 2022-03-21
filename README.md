# bandcamp-flac-get (bcfg)
Generate flac/mp3/vorbis download links for bandcamp albums that are free (or name your own price with no minimum price). It will download a zip with cover image, metadata, and files organized into folders.

It will use automation software to open up your browser and navigate to every album.
It will start finding the places to click to open up a download dialog, and will gather the links required to do these downloads. When it's done scraping, the browser will close, and in your command line you will see progress bars as the downloads begin.

It will batch download all the links you have on each line of a text file:



# Simple Installation

---

#### **Currently the only supported OS is Linux and the only supported browsers are chrome/chromium.**

---

## Debian and Ubuntu

These commands are intended for people that have trouble getting it working.
They make sure that python is installed and make sure that google-chrome is available.
Its binary path can be found using `which google-chrome.`

```bash
sudo apt update
sudo apt install python3 python3-pip 
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
which google-chrome
```

Make a note of that path is shows you.

---

# Confiuguration And Settings

You have to tell the program where the browser binary is, what browser you're using, what type of files you want to download (mp3, flac, etc), as well as the path to the download directory.
You can type this to begin setting it up in your terminal...

```bash
bash ./LINUX_SETUP.sh
```

...or you can just open the settings files. They are found here:
+ **SETTINGS FILE**: `src/bcfg/example.py`
+ **EXAMPLE**: `src/bcfg/settings_example.py`

Make the settings file look like the example. Follow the instructions in the file.

## Add Files To Download List

This file (or whatever file you configured to use in the settings) is where you will list urls to albums to be downloaded.
Each link should be on its own line and have `"bandcamp.com/album/"` somewhere in it.

**DEFAULT DOWNLOAD LIST**: `album_links.txt`

```
https://digi4.bandcamp.com/album/--2
https://kekal.bandcamp.com/album/deeper-underground
https://demondice.bandcamp.com/album/shut-up-get-happy
```

# Finally! Try It Out

Once those two/three things are done, all you need to do is: 

```bash
bash ./LINUX_START_DOWNLOADING.sh
```

If everything is done right, it should just start doing it for you.
I recommend watching the program run and not doing an absurd amount of downloads at once in one job. The most I have tested at one time is about 25-35.

## FAQ

### What do I do if BandCamp stops on one of the download links and says it's having trouble processing and to try again?
Wait 30 seconds to 90 seconds. And click the "Try Again" link without touching any other links or navigating away from page.
If it says the same thing again, just wait. In a few minutes, try clicking "Try Again". 

Do it as many times as you need to. It's reacting to you hitting the servers repeatedly over and over again, 
so just stop for a second. Just wait and watch the program where it says, "Having trouble processing, Try Again."

In the background, the script is waiting for the download link to appear. But it's not impatient. The 
default `TIMEOUT_TIME` found in `src/bcfg/settubgs.py` is `1000000000` seconds, so it isn't going to error out on you. 
You can also change this if you would like to

In my testing, there was never more than a couple of minutes at most required. I only ever saw this happen as a result 
of testing it over and over again, which the answer to what you should do here: Just Wait. Only Click Try Again. 
When it works, the script will take over. If it doesn't (because you have changed the page by clicking things), 
you will need to kill the process and start over. 

### Why does the program skip some links?

The Three links in the example `album_links.txt` files demonstrates three different things the script handles:

1) a free album, 
2) a name your own price with no minimum album, 
3) and an album that will only provide the flac versions of the songs if you purchase it. 

The program will work perfectly on the first two and will simply skip any album that it cannot get for free.

I recommend that you support artists where you can regardless as they are often not asking for very much on sites 
like BandCamp. If you are looking for a 
tool that allows you to batch download flacs for albums *you have* paid for and that are not *specifically free*, 
you might be interested in [bandcamp-collection-downloader](https://github.com/Ezwen/bandcamp-collection-downloader)


### Is my device/browser is not supported?

1) have not messed with using this on Windows yet. Eventually I will have an `install_windows` script, but at this point, I have not even tested this on Windows. It will happen though... Eventually.   
2) have not added support for any other browser besides Chrome and Chromium. There are options for the other browsers but I don't think they will work effectively without some more tinkering.

If you do have a problem with trying to set it running, feel free to use the [issue tracker](https://github.com/shaenr/bandcamp-flac-get/issues) to let me know what problem you're having and/or make a pull request.

### What are these files in the utils that start with `utils/bcfg-` and end with `.sh`
They're small utilities in a language called bash that you might find useful if you're a complete nerd, but 
they have nothing to do with the scraping and downloading of albums exactly.

Those are not directly used by the python3 script, which does all the work of scraping and downloading, and as of this time is entirely contained in `bcfg/__init__.py`.
There is a `main.py` file but as of this commit, it is just a caller of the bcfg package.

They're mainly used for either pre-processing HTML pages to generate album links or post-processing 
to do something with the flac file zips after they're downloaded.

I honestly do not recommend using these if you do 
not care to figure out how to use them for yourself, but... 
I included them because they were written to make use of this tool better in a couple ways for my individual needs.

More information is available in the files themselves.

- [bcfg-album2mkv.sh](https://github.com/shaenr/bandcamp-flac-get/blob/main/bcfg-album2mkv.sh) -- This script generates a single flac file from all the flacs in an album zip archive downloaded from bandcamp.
If the flac files for different songs are not rendered using the same sample rate, the script will find the most
common sample rate among them to use and convert the smallest amount of files to make them compatible.
Using that single flac file, an mkv video is generated using the cover art for the visual. The remaining files
left over after the process are then removed.
- [bcfg-artist2discog.sh](https://github.com/shaenr/bandcamp-flac-get/blob/main/bcfg-artist2discog.sh) -- This script is much simpler. Basically you just pass it an artist link; in the command console, like this: `bash bcfg-artist2discog.sh windows96.bandcamp.com`". If you do it right, it will add every album the artist has uploaded to their BandCamp page to your `album_links.txt`
- The other files are utility functions used in the other bash scripts.

# GNU General Public License v3.0

If you did not receive a copy you can find the [LICENSE](https://github.com/shaenr/bandcamp-flac-get/blob/main/LICENSE) here. 