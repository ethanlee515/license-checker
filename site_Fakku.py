#!/usr/bin/env python3.7

import requests
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
		while status == 200:
			soup = BeautifulSoup(text, 'html.parser')
			titles = soup.find_all(class_='content-title')
			for title in titles:
				results.append(title.decode_contents())
			page += 1
			status, text = await fetch_page(session, author, page)
		if status != 404:
			raise Exception("Interrupted somehow")
		return results

def build_url(author, page):
	return f'http://fakku.net/search/{author}/page/{page}'

async def fetch_page(session, author, page):
	async with session.get(build_url(author, page)) as response:
		return (response.status, await response.text())

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3 site_Fakku.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
