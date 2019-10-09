# license-checker
Checks if a particular manga is licensed in English by looking it up on a given set of sites. The user interface is a Discord bot.
## Dependencies
* Python 3.7.3+
* The libraries below
	* BeautifulSoup
	* numpy
	* discord.py
	* tensorflow
## Setup
* Modify the top of `similarity.py` depending on your tensorflow version.
	* To find out the version number, do `python3.7 -c "import tensorflow;print(tensorflow.__version__)"`
	* Pip3.7+ should download 2.0+ by default.
* Execute `python3.7 similarity.py` to download/cache the tensorflow module
* Create bot-token.txt and put your token in there
## Running
* Execute `python3.7 main.py`
* Give the Discord bot commands of the form `.lc "author" "title"` or `.lc -a author -t title`
## Sites and status
* [2DMarket](http://2d-market.com/): Works in progress. Requires site login to search.
* [Comic Bavel](https://comicbavel.com/): No English version exists.
* Comic Europa: Official site possibly [here](http://comicbavel.com/europa/)? No English versions though.
* Comic Hana-Man: Published through [Wanimagazine](https://www.wani.com/) which has no English version.
* Comic Kairakuten: Published through [Wanimagazine](https://www.wani.com/) which has no English version.
* Comic Kairakuten Beast: Published through [Wanimagazine](https://www.wani.com/) which has no English version.
* Comic Koh: Can't find official site?
* Comic Shitsurakuten: Published through [Wanimagazine](https://www.wani.com/) which has no English version.
* Comic X-Eros: Published through [Wanimagazine](https://www.wani.com/) which has no English version.
* [Fakku](https://www.fakku.net/): Work in progress.
* Girls forM: Can't find official site?
* Hana-Man Gold: Published through [Wanimagazine](https://www.wani.com/) which has no English version.
* [Project Hentai](https://www.projecthentai.com/); work in progress.
* ENSHODO: Closed permanently. [Source](https://www.twipu.com/patinafinish/tweet/1167021110849703937)
## Examples
TODO
