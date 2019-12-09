#!/usr/bin/env python3.7

import sys
import asyncio

name = "2D Market"
async def get_manga_by_author(author):
	proc = await asyncio.create_subprocess_exec(
			"./2D_Market.py",
			author,
			stdout=asyncio.subprocess.PIPE)
	await proc.wait()
	results = list()
	while True:
		line = (await proc.stdout.readline()).decode().strip()
		if len(line) == 0:
			break
		results.append(line)
	return results
	

if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3 site_2D_Market.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
