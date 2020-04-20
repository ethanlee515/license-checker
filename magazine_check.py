import re
from bs4 import BeautifulSoup
import aiohttp


def date_compare(magazine, issue):
	global licensed_magazines
	startdate = licensed_magazines[magazine][1]

	# enddate not required for this impl of date compare, because all magazines that are licensed have no end date
	# enddate = licensed_magazines[magazine][2]

	pattern = re.compile(r"(\d+)-(\d+)")
	match = re.match(pattern, issue)
	match2 = re.match(pattern, startdate)

	issueyear = int(match.group(1))
	issuemonth = int(match.group(2))

	startyear = int(match2.group(1))
	startmonth = int(match2.group(2))

	if startyear > issueyear:
		return False
	elif startyear == issueyear and startmonth < issuemonth:
		return False
	return True


def num_compare(magazine, issue):
	global licensed_magazines
	startnum = licensed_magazines[magazine][1]
	endnum = licensed_magazines[magazine][2]

	if endnum == -1:
		endnum = 100000000

	issuenum = int(issue.strip().strip("#"))

	return startnum <= issuenum <= endnum


def always_licensed(magazine, issue):
	return True


licensed_magazines = {
	"kairakuten" : [date_compare, "2015-06", "now"],
	"x-eros" : [num_compare, 30, -1],
	"shitsurakuten" : [date_compare, "2016-04", "now"],
	"kairakuten beast" : [date_compare, "2016-12", "now"],
	"bavel": [always_licensed],
	"europa": [num_compare, 11, -1],
	"girls form": [num_compare, 13, 16],
	"happining": [always_licensed],
	"aoha": [always_licensed],
	"weekly kairakuten": [always_licensed],
	"dascomi": [always_licensed],
	"koh": [num_compare, 1, 2]
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


async def check_link(link):
	title = await get_title(link)

	# Make the title lowercase
	title = title.lower()

	# See if this doujin has a magazine associated with it
	# (girls forM is annoying because it doesn't have a COMIC, so I have to use another regex)
	pattern1 = re.compile(r".*\(\s*comic\s*(.+?)\s*(?:vol\.)?\s*((\d|-|#)*)\)")
	pattern2 = re.compile(r".*\(\s*girls\s*form\s*(?:vol\.)?\s*(\d+)\)")

	magazine_name = None
	magazine_issue = None

	match1 = re.match(pattern1, title)
	match2 = re.match(pattern2, title)

	# Extract the magazine issue and name
	if match1 is not None:
		magazine_name = match1.group(1).lower()
		magazine_issue = match1.group(2)
	# again, girls forM special handling
	elif match2 is not None:
		match2 = re.match(pattern2, title)
		magazine_name = "girls form"
		magazine_issue = match2.group(1).lower()

	licensed = False

	# If this is in a licensed magazine, check if it's in a licensed issue
	if magazine_name in licensed_magazines:
		licensed = licensed_magazines[magazine_name][0](magazine_name, magazine_issue)

	if licensed:
		return magazine_name.upper() + " " + magazine_issue
	else:
		return None
