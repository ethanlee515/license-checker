#!/usr/bin/env python3.7

import sys
import asyncio
import urllib

name = "2D Market"
async def get_manga_by_author(author):
	raise NotImplementedError
	async with aiohttp.ClientSession() as session:
		resp = await session.get(
				'https://2d-market.com/Search?search_value=' +
				urllib.parse.quote_plus(author) +
				'&type=author')
		text = await resp.text()
		soup = BeautifulSoup(text, 'html.parser')
		# authors = 



	

	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3 site_2D_Market.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
