import re
from bs4 import BeautifulSoup
import aiohttp


def date_num_compare(magazine, issue):
	global licensed_magazines

	if " " in issue:
		issue = issue.split(" ")[0]

	pattern = re.compile(r"(\d+)-(\d+)")
	pattern2 = re.compile(r"\D*(\d+)\D*")

	match = re.match(pattern, issue)
	match2 = re.match(pattern2, issue)

	if match is not None:
		startdate = licensed_magazines[magazine][1]
		enddate = licensed_magazines[magazine][2]

		startmatch = re.match(pattern, startdate)
		endmatch = re.match(pattern, enddate)

		issueyear = int(match.group(1))
		issuemonth = int(match.group(2))

		startyear = int(startmatch.group(1))
		startmonth = int(startmatch.group(2))

		endyear = int(endmatch.group(1))
		endmonth = int(endmatch.group(2))

		if startyear > issueyear or issueyear > endyear:
			return False
		elif startyear == issueyear and startmonth > issuemonth:
			return False
		elif endyear == issueyear and endmonth < issuemonth:
			return False
		return True
	else:
		startnum = licensed_magazines[magazine][3]
		endnum = licensed_magazines[magazine][4]

		if endnum == -1:
			endnum = 100000000

		issuenum = int(match2.group(1))

		return startnum <= issuenum <= endnum


def always_licensed(magazine, issue):
	return True


licensed_magazines = {
	"kairakuten": [date_num_compare, "2015-06", "9999-99", None, None],
	"x-eros": [date_num_compare, None, None, 30, -1],
	"shitsurakuten": [date_num_compare, "2016-04", "9999-99", None, None],
	"kairakuten beast": [date_num_compare, "2016-12", "9999-99", None, None],
	"bavel": [always_licensed],
	"europa": [date_num_compare, "2017-04", "9999-99", 11, -1],
	"girls form": [date_num_compare, None, None, 13, 16],
	"happining": [always_licensed],
	"aoha": [always_licensed],
	"weekly kairakuten": [always_licensed],
	"dascomi": [always_licensed],
	"koh": [date_num_compare, "2013-12", "2014-07", 1, 2]
}


# Returns the title of a doujin
async def get_title(link):
	# Input validation / pre-processing
	link = link.lower()
	if link[:7] == "http://":
		link = "https://" + link[7:]
	if "nhentai.net/g/" not in link:
		raise Exception("Invalid link")
	if not link[-1] == "/":
		link = link + "/"

	async with aiohttp.ClientSession() as session:
		resp = await session.get(link)
		page = await resp.text()
		soup = BeautifulSoup(page, 'html.parser')
		titles = soup.find_all('h1')

		return str(titles[0])


async def get_title_japanese(link):
	# Input validation / pre-processing
	link = link.lower()
	if link[:7] == "http://":
		link = "https://" + link[7:]
	if "nhentai.net/g/" not in link:
		raise Exception("Invalid link")
	if not link[-1] == "/":
		link = link + "/"

	async with aiohttp.ClientSession() as session:
		resp = await session.get(link)
		page = await resp.text()
		soup = BeautifulSoup(page, 'html.parser')
		titles = soup.find_all('h2')

		title_japanese = str(titles[0])

		pattern_extractor = re.compile(r"(?:\s*[<\[({].*?[\])}>]\s*)*([^\[\](){}<>]*)(?:\s*[<\[({]/?.*?[\])}>]\s*)*$")
		match = re.match(pattern_extractor, title_japanese.strip())

		return match.group(1)


async def check_link(link):
	title = await get_title(link)

	# Make the title lowercase
	title = title.lower()

	# See if this doujin has a magazine associated with it
	# (girls forM is annoying because it doesn't have a COMIC, so I have to use another regex)
	# (so is Weekly Kairakuten)
	pattern1 = re.compile(r".*\(\s*comic\s*(.+?)\s*(?:vol\.)?\s*((\d|-|#|,|\s)*)\)")
	pattern2 = re.compile(r".*\(\s*girls\s*form\s*(?:vol\.)?\s*(.+?)\)")
	pattern3 = re.compile(r".*\(\s*weekly\s*kairakuten\s*(?:vol\.)?\s*(.+)\)")

	magazine_name = None
	magazine_issue = None

	match1 = re.match(pattern1, title)
	match2 = re.match(pattern2, title)
	match3 = re.match(pattern3, title)

	# Extract the magazine issue and name
	if match1 is not None:
		magazine_name = match1.group(1).lower()
		magazine_issue = match1.group(2)
	# again, girls forM special handling
	elif match2 is not None:
		magazine_name = "girls form"
		magazine_issue = match2.group(1).lower()
	# special handling for kairakuten weekly
	elif match3 is not None:
		magazine_name = "weekly kairakuten"
		magazine_issue = match3.group(1).lower()

	# handle any wacky
	if magazine_issue is not None and "," in magazine_issue:
		magazine_issue = magazine_issue.split(",")[0].strip()

	licensed = False

	# If this is in a licensed magazine, check if it's in a licensed issue
	if magazine_name in licensed_magazines:
		licensed = licensed_magazines[magazine_name][0](magazine_name, magazine_issue)

	if licensed:
		return magazine_name.upper() + " " + magazine_issue
	else:
		return None