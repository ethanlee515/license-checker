#!/usr/bin/env python3.7

import sys
import asyncio
import urllib
import aiohttp
import itertools
from bs4 import BeautifulSoup

name = "2D Market"
async def get_manga_by_author(author):
	async with aiohttp.ClientSession() as session:
		resp = await session.get(
				'https://2d-market.com/Search?search_value=' +
				urllib.parse.quote_plus(author) +
				'&type=author')
		page = await resp.text()
		soup = BeautifulSoup(page, 'html.parser')
		author_link_tags = soup.select('.showcase_author_name h1 a')
		author_links = map(lambda tag: tag['href'], author_link_tags)

		results = list()
		for author_link in author_links:
			for page_num in itertools.count(1):
				resp = await session.get(
						f'https://2d-market.com{author_link}?page={page_num}')
				page = await resp.text()
				soup = BeautifulSoup(page, 'html.parser')
				elements = soup.select(
						'.showcase_comics_product_info hgroup h1 a')
				if len(elements) == 0:
					break
				for element in elements:
					results.append(element.decode_contents())
		return results
	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3.7 site_2D_Market.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
