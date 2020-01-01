# license-checker
Checks if a particular manga is licensed in English by looking it up on a given set of sites.
Built for the [r/wholesomehentai](https://reddit.com/r/wholesomehentai) subreddit and its associated Discord server.
## Dependencies
* Python 3.7 with pip 19.0+
* Firefox
* [geckodriver](https://github.com/mozilla/geckodriver/releases)
## Setup
* Ensure that the command `python3.7` in fact points to Python 3.7
* Execute `pip install -r dependencies.txt`
* Execute `./similarity.py < test_sim.txt` to cache and test the tensorflow module (might take a while to download)
* Create bot-token.txt and put your token in there
* Run `./Project_Hentai.py girl` to test your selenium installation. This should pull up the search results for "girl" from Project Hentai.
## Running
* Execute `./main.py`
* Give the Discord bot commands of the form `.lc "author" "title"` or `.lc -a author -t title`
## Sites and status
* [2DMarket](http://2d-market.com/): Done!
* [Comic Bavel](https://comicbavel.com/): No English version exists.
* Comic Europa: Official site possibly [here](http://comicbavel.com/europa/)? No English versions though.
* Comic Hana-Man: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* Comic Kairakuten: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* Comic Kairakuten Beast: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* Comic Koh: Can't find official site?
* Comic Shitsurakuten: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* Comic X-Eros: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* [Fakku](https://www.fakku.net/): Done!
* Girls forM: Can't find official site?
* Hana-Man Gold: Published through [Wanimagazine](https://www.wani.com/) which has no English site.
* [Project Hentai](https://www.projecthentai.com/): Done!
* ENSHODO: Closed permanently. [Source](https://www.twipu.com/patinafinish/tweet/1167021110849703937)
