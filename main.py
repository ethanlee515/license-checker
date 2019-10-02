#!/usr/bin/env python3.7

import sys
import discord
import asyncio
import re
import functools
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

cmd_prefix = re.compile(r"\.lc(:?\s+.*)?$")
cmd_pattern1 = re.compile(r'\.lc\s+"([^"]+)"\s+"([^"]+)"$')
cmd_pattern2 = re.compile(r"\.lc\s+-(.)\s+(.+)\s+-(.)\s+(.+)$")

async def edit_status(msg, name, status):
	await msg.edit(content=
			re.sub(f'{name}:.*', f'{name}: {status}', msg.content))

@lc.event
async def on_message(message):
	if not cmd_prefix.match(message.content):
		return
	content = message.content.strip().replace('“','"').replace('”','"')
	author = None
	title = None
	match1 = cmd_pattern1.match(content)
	match2 = cmd_pattern2.match(content)
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
		asyncio.create_task(message.channel.send('Invalid command. '
			'Usage: `.lc "author" "title"` or `.lc -a author -t title`'))
		return
	msg = await asyncio.create_task(message.channel.send(
		functools.reduce(
			lambda m, site: m + f'\n{site.name}: Please wait...',
			site_modules, f'Looking up {title} by {author}.')))
	await asyncio.sleep(2)
	await edit_status(msg, 'Comic Bavel', 'STATUS EDIT TEST')
	await asyncio.sleep(2)
	await edit_status(msg, 'Comic Hana-Man', 'STATUS EDIT TEST 2')
	await asyncio.sleep(2)
	await edit_status(msg, 'Comic Koh', 'STATUS EDIT TEST 3')

@lc.event
async def on_ready():
	print("bot is running...")

lc.run(token)
