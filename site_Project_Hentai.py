#!/usr/bin/env python3.8

import sys
import asyncio

name = "Project Hentai"


async def get_manga_by_author(author):
	proc = await asyncio.create_subprocess_exec(
		"./Project_Hentai.py",
		author,
		stdout=asyncio.subprocess.PIPE)
	stdout, stderr = await proc.communicate()
	return stdout.decode().split('\n')


if __name__ == "__main__":
	if len(sys.argv) != 2:
		print('usage: python3.8 Project_Hentai.py "author name"')
		exit(1)
	print(asyncio.run(get_manga_by_author(sys.argv[1])))
