# license-checker
Checks if a particular manga is licensed in English by looking it up on a given set of sites.
Built for https://wholesomelist.herokuapp.com/ (which stemmed from the [r/wholesomehentai](https://reddit.com/r/wholesomehentai) subreddit) and its associated Discord server.
## Dependencies
* Unix (MacOS/Linux); this bot doesn't work on Windows due to TensorFlow-text having no WIndows installation
* Python 3.9 with pip 19.0+
* Firefox
* [geckodriver](https://github.com/mozilla/geckodriver/releases)
## Setup
* Ensure that the command `python3.9` in fact points to Python 3.9
* Execute `python3.9 -m pip install -r dependencies.txt`. You probably need `sudo` permission.
* Execute `./similarity.py < test_sim.txt` to cache and test the tensorflow module (might take a while to download)
* Create bot-token.txt and put your token in there
* Run `./Project_Hentai.py girl` to test your selenium installation. This should pull up the search results for "girl" from Project Hentai.
## Running
* Execute `./main.py`
* Give the Discord bot commands of the form `.lc "author" "title" "link" (-en | -jp)` or `.lc -a author -t title -l link (-en | -jp)`
## Sites and status
* [2DMarket](http://2d-market.com/): Done!
* [Comic Bavel](https://comicbavel.com/): No English version exists. Licensed releases: `All of them.`
* Comic Europa: Official site possibly [here](http://comicbavel.com/europa/)? Licensed releases: `Vol. 11 onwards`
* Comic Hana-Man: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* Comic Kairakuten: Published through [Wanimagazine](https://www.wani.com/). Licensed releases: `Issue 2015-06 onwards`
* Comic Kairakuten Beast: Published through [Wanimagazine](https://www.wani.com/). Licensed releases: `Issue 2016-12 onwards`
* Comic Koh: Can't find official site? Licensed releases: `Vol. 1-2`
* Comic Shitsurakuten: Published through [Wanimagazine](https://www.wani.com/). Licensed releases: `Issue 2016-04 onwards`
* Comic X-Eros: Published through [Wanimagazine](https://www.wani.com/). Licensed releases: `Vol. 30 onwards`
* [Fakku](https://www.fakku.net/): Done!
* Girls forM: Can't find official site? Licensed releases: `Vol. 13-16`
* Hana-Man Gold: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* Comic Happining: Licensed releases: `All of them.`
* Comic Aoha: Licensed releases: `All of them.`
* Dascomi: Licensed releases: `All of them.`
* [Project Hentai](https://www.projecthentai.com/): Done!
* ENSHODO: Closed permanently. [Source](https://www.twipu.com/patinafinish/tweet/1167021110849703937)
