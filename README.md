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
* 2DMarket: **NYI** Requires site login to search
* Comic Bavel: [Site](https://comicbavel.com/) has no English version.
* Comic Europa: Can't find official site?
* Comic Hana-Man: [Site](https://www.wani.com/product/03777/) has no English version.
* Comic Kairakuten: Can't find official site?
* Comic Kairakuten Beast: Can't find official site?
* Comic Koh: Can't find official site?
* Comic Shitsurakuten: Can't find official site?
* Comic X-Eros: **NYI**
* Fakku: [Site]("https://www.fakku.net/"); work in progress.
* Girls forM: Can't find official site?
* Hana-Man Gold: **NYI**
* Project Hentai: [Site](https://www.projecthentai.com/); work in progress.
* ENSHODO: [Site](https://www.twipu.com/patinafinish/tweet/1167021110849703937) closed permanently
## Examples
TODO
