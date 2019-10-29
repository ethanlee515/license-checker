#!/usr/bin/env python3.7
name = "Project Hentai"

import re
import sys
import asyncio
import requests

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

async def get_manga_by_author(author):
	options = Options()
	options.headless = True
	driver = webdriver.Firefox(options=options)
	driver.implicitly_wait(10)
	driver.get('https://www.projecthentai.com')
	results = list()
	driver.find_element_by_css_selector(
			'//iframe//.ecwid-search-widget__input') \
			.send_keys(author, Keys.ENTER)
	url = driver.getCurrentUrl()

	



	# TODO The above doesn't work because of iframe shenanigans
	'''
	soup = BeautifulSoup(site, 'html.parser')
	results_count = int(re.search(r"of (\d+) items",
		soup.find(class_='pager__count-pages')).group(1))
	'''

	driver.quit()

	return url
	
	# params += '&offset=60'

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3 site_Project_Hentai.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
