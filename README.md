# bandcamp-flac-get (bcfg)
Generate flac download links for bandcamp albums that are free (or name your own price with no minimum price).

It will use automation software to open up your browser and navigate to every album on your list, where it will start finding the places to click to open up a download dialog, and will gather the links required to do these downloads. When it's done scraping, the browser will close, and in your command line you will see progress bars as the downloads begin.

It will batch download all the links you have on each line of a text file: `album_links.txt`.

It works fairly well, but overall it's rudimentary and requires some knowledge of what to do to get the best out of it.

I will try to show you everything below.

# Installation
Once you have Python3 installed and have navigated to the project directory in your command line, you can do:

```
python3 -m pip install -r requirements.txt
```


If you are on Windows, I believe this command could be `py` or `python` instead of 'python3'. But it's otherwise the same.

# Setup

If you're on Linux (or Mac), you can do `bash install_linux.sh` and running that script 
will result in a new 
file appearing in your project: `.env`.

If you use the `install_linux.sh` script, it should give you something like this:

**FILE:** `.env`

```dotenv
DOWNLOAD_PATH=/home/shaenr
CHROME_BINARY=/usr/bin/google-chrome
```

You don't really need that script to generate this `.env` file, whether you have Linux or not. The only thing you need is:

1) create a file 
called `.env` and put it inside the main project directory, which should be `bandcamp-flac-get`. 

2) Then copy those two lines and paste them into the file. But find and use the correct paths to your folder and your installed version of Chrome/Chromium instead of the ones in my example.

If you're on Windows, most likely your paths will look a bit different. But you plug them in there exactly the same way.

---

The `DOWNLOAD_PATH` is where the massive zips are going to accumulate.

The `CHROME_BINARY` is literally the path to the browser we are going to use to automate getting the tokenized links to the flac downloads.
On Linux you can do `where chromium` or whatever alias you're using if I didn't find the right one for you already. 

---

**On Windows it would be something like**

    %ProgramFiles%\Google\Chrome\Application\chrome.exe
    or C:\Program Files (x86)\Google\Application\chrome.exe

You get the idea. You need the *absolute path* to those things in that file.

### One Last File: the Download Queue

This file is where you will list batch jobs for the script in the form of links; one link per line, and each 
link should have `bandcamp.com/album/` somewhere in it.

**FILE:** `album_links.txt`

```
https://digi4.bandcamp.com/album/--2
https://kekal.bandcamp.com/album/deeper-underground
https://demondice.bandcamp.com/album/shut-up-get-happy

```

Three links here demonstrate three different things the script handles.

1) a free album, 
2) a name your own price with no minimum album, 
3) and an album that will only provide the flac versions of the songs if you purchase it. 

The program will work perfectly on the first two and will simply skip any album that it cannot get for free.

I recommend that you support artists where you can regardless as they are often not asking for very much on sites 
like BandCamp. If you are looking for a 
tool that allows you to batch download flacs for albums *you have* paid for and that are not *specifically free*, 
you might be interested in [bandcamp-collection-downloader](https://github.com/Ezwen/bandcamp-collection-downloader)

# Finally! Try It Out

Once those two/three things are done, all you need to do is: `python3 main.py` from the project directory. If everything is done right, it should just start doing it for you.
I recommend watching the program run and not doing an absurd amount of downloads at once in one job. The most I have tested at one time is about 25-35.

## FAQ

### What do I do if BandCamp stops on one of the download links and says it's having trouble processing and to try again?
Wait 30 seconds to 90 seconds. And click the "Try Again" link without touching any other links or navigating away from page.
If it says the same thing again, just wait. In a few minutes, try clicking "Try Again". 

Do it as many times as you need to. It's reacting to you hitting the servers repeatedly over and over again, 
so just stop for a second. Just wait and watch the program where it says, "Having trouble processing, Try Again."

In the background, the script is waiting for the download link to appear. But it's not impatient. The 
default `TIMEOUT_TIME` found in `main.py` is `1000000000` seconds, so it isn't going to error out on you. 
You can also change this if you would like to

In my testing, there was never more than a couple of minutes at most required. I only ever saw this happen as a result 
of testing it over and over again, which the answer to what you should do here: Just Wait. Only Click Try Again. 
When it works, the script will take over. If it doesn't (because you have changed the page by clicking things), 
you will need to kill the process and start over. 

### What do I do if I'm not using Linux?

1) have not messed with using this on Windows yet. Eventually I will have an `install_windows` script, but at this point, I have not even tested this on Windows. It will happen though... Eventually.   
2) have not added support for any other browser besides [Chromium](https://www.chromium.org/getting-involved/download-chromium/). I will eventually add FireFox but as of now, I have only tested this with Chromium.

If you do have a problem with trying to set it running, feel free to use the [issue tracker](https://github.com/shaenr/bandcamp-flac-get/issues) to let me know what problem you're having and/or make a pull request.

### It's saying something in the console about not having web drivers.

You shouldn't have this problem because it automatically finds the correct drivers for your version of your 
browser every time you start it. But knowing software, it'll happen to someone. If for some reason it does 
say something like that, you want the exactly correct version of [ChromeDriver](https://chromedriver.chromium.org/downloads) 
for your exactly correct version of Chrome that you are using in the `CHROME_BINARY` option in the `.env` file.

You have to make sure that this file that you get is in a location that is on the system `$PATH`.

If all else fails, I recommend asking yourself if you've installed a new version of Chrome recently and if that might
make it easier for you in that event.

### What are these files that start with `bcfg-` and end with `.sh`
They're small utilities in a language called bash that you might find useful if you're a complete nerd, but 
they have nothing to do with the scraping and downloading of albums exactly.

Those are not directly used by the python3 script, which does all the work of scraping and downloading, and as of this time is entirely contained in `main.py`.

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