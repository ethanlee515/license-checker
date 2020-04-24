#!/usr/bin/env python3.7

import sys
import asyncio
import aiohttp
from bs4 import BeautifulSoup

name = "Fakku"


async def get_manga_by_author(author):
	results = list()
	page = 1
	async with aiohttp.ClientSession() as session:
		status, text = await fetch_page(session, author, page)

		# It is noteworthy that FAKKU oftentimes does not return the same results each time for searches,
		# so I made this search by author URL instead.
		# Somehow, getting doujins by author instead of search seems to be more reliable.
		# However, I'm really not sure why.
		while "There is no content available at this time" not in text and not status == 404:
			soup = BeautifulSoup(text, 'html.parser')
			titles = soup.find_all(class_='content-title')
			for title in titles:
				results.append(title.decode_contents())
			page += 1
			status, text = await fetch_page(session, author, page)
		return results


def build_url(author, page):
	author = author.replace(" ", "-")
	if page == 1:
		return f'http://fakku.net/artists/{author}'
	else:
		return f'http://fakku.net/artists/{author}/page/{page}'


async def fetch_page(session, author, page):
	async with session.get(build_url(author, page)) as response:
		return response.status, await response.text()


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3 site_Fakku.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
