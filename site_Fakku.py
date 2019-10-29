#!/usr/bin/env python3.7

import requests
import sys
import asyncio
from bs4 import BeautifulSoup

name = "Fakku"
async def get_manga_by_author(author):
	results = list()
	page_num = 1
	response = requests.get(f'http://fakku.net/search/{author}/page/1')
	while response:
		soup = BeautifulSoup(response.text, 'html.parser')
		titles = soup.find_all(class_='content-title')
		for title in titles:
			results.append(title.decode_contents())
		page_num += 1
		response = requests.get(
				f'http://fakku.net/search/{author}/page/{page_num}')
	if response.status_code != 404:
		raise Exception("Interrupted somehow")
	return results

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3 site_Fakku.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
