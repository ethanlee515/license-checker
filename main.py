#!/usr/bin/env python3.7

import sys
import discord
import asyncio
import re
import functools
from similarity import compute_similarity
import site_2D_Market
import site_Comic_Bavel
import site_Comic_Europa
import site_Comic_HanaMan
import site_Comic_Kairakuten
import site_Comic_Kairakuten_Beast
import site_Comic_Koh
import site_Comic_Shitsurakuten
import site_Comic_XEros
import site_Fakku
import site_Girls_forM
import site_HanaMan_Gold
import site_Project_Hentai
import site_ENSHODO

site_modules = [site_2D_Market, site_Comic_Bavel, site_Comic_Europa,
	site_Comic_HanaMan, site_Comic_Kairakuten, site_Comic_Kairakuten_Beast,
	site_Comic_Koh, site_Comic_Shitsurakuten, site_Comic_XEros, site_Fakku,
	site_Girls_forM, site_HanaMan_Gold, site_Project_Hentai, site_ENSHODO]

try:
	with open("bot-token.txt", "r") as token_file:
		token = token_file.read().strip()
except FileNotFoundError:
	print("Cannot open bot-token.txt", file=sys.stderr)
	exit(1)

lc = discord.Client()

async def check_site(site, author, title):
	# TODO
	await asyncio.sleep(5)
	raise NotImplementedError()
	return "placeholder done status result"

async def process_site(site, author, title, channel):
	msg = await channel.send(f"{site.name}: Please wait...")
	try:
		status = await check_site(site, author, title)
	except Exception as e:
		if str(e):
			status = f'{type(e).__name__} - {e}'
		else:
			status = type(e).__name__
	await msg.edit(content=f"{site.name}: {status}")

@lc.event
async def on_message(msg):
	if not re.match(r"\.lc(:?\s+.*)?$", msg.content):
		return
	content = msg.content.strip().replace('“','"').replace('”','"')
	author = None
	title = None
	match1 = re.match(r'\.lc\s+"([^"]+)"\s+"([^"]+)"$', content)
	match2 = re.match(r"\.lc\s+-(.)\s+(.+)\s+-(.)\s+(.+)$", content)
	if match1:
		author = match1.group(1)
		title = match1.group(2)
	elif match2:
		for i in (1, 3):
			if match2.group(i) == 'a':
				author = match2.group(i + 1).strip().strip('"')
			elif match2.group(i) == 't':
				title = match2.group(i + 1).strip().strip('"')
	if author is None or len(author) == 0 or title is None or len(title) == 0:
		asyncio.create_task(msg.channel.send('Invalid command. '
			'Usage: `.lc "author" "title"` or `.lc -a author -t title`'))
		return
	await msg.channel.send(f"Looking up {title} by {author}.")
	for site in site_modules:
		asyncio.create_task(process_site(site, author, title, msg.channel))

@lc.event
async def on_ready():
	print("bot is running...")

lc.run(token)
