#!/usr/bin/env python3.7
name = "Project Hentai"

import binascii
import re
import sys
import asyncio
from bs4 import BeautifulSoup
import requests

async def get_manga_by_author(author):
	params = f'search?keyword={author}'
	hex_params = binascii.hexlify(str.encode(params))
	url = f'https://www.projecthentai.com/online-store/hex%3A{hex_params}'
	
	site = requests.get(url).text
	# TODO The above doesn't work because the site is rendered dynamically
	soup = BeautifulSoup(site, 'html.parser')
	results_count = int(re.search(r"of (\d+) items",
		soup.find(class_='pager__count-pages')).group(1))

	return results_count
	
	# params += '&offset=60'

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3 site_Project_Hentai.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
