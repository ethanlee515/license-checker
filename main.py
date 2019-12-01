#!/usr/bin/env python3.7

import sys
import discord
import asyncio
import re
import functools
# from similarity import compute_similarity
# import site_test_debug
import site_2D_Market
import site_Fakku
import site_Project_Hentai
import json
import traceback

site_modules = [site_2D_Market, site_Fakku, site_Project_Hentai]
# site_modules.append(site_test_debug)

try:
	with open("bot-token.txt", "r") as token_file:
		token = token_file.read().strip()
except FileNotFoundError:
	print("Cannot open bot-token.txt", file=sys.stderr)
	exit(1)

# TODO Consider refactoring bot into a class to eliminate globals
lc = discord.Client()

pending_msgs = dict()
sim_calc = None

async def process_site(site, author, title, channel):
	msg = await channel.send(f"{site.name}: fetching titles...")
	try:
		titles = await site.get_manga_by_author(author)
		await msg.edit(content=f"{site.name}: comparing titles...")
		pending_msgs[msg.id] = {"message": msg, "site": site.name}
		req = {"title": title, "titles": titles, "message_id": msg.id}
		sim_calc.stdin.write((json.dumps(req) + '\n').encode('utf-8'))
	except Exception as e:
		traceback.print_exc()
		if str(e):
			status = f'{type(e).__name__} - {e}'
		else:
			status = type(e).__name__

@lc.event
async def on_message(msg):
	content = msg.content.strip().replace('“','"').replace('”','"')
	if not re.match(r"\.lc(:?\s+.*)?$", content):
		return
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

async def recv_sim_calc():
	global pending_msgs
	while True:
		line = await sim_calc.stdout.readline()
		results = json.loads(line)
		m = pending_msgs[results["message_id"]]
		msg = m["message"]
		site = m["site"]
		await msg.edit(content=f"{site}: {line.decode('utf-8')}")

@lc.event
async def on_ready():
	print("bot is running...")

async def main():
	print("starting subprocess")
	global sim_calc
	sim_calc = await asyncio.create_subprocess_exec(
			"./similarity.py",
			stdin=asyncio.subprocess.PIPE,
			stdout=asyncio.subprocess.PIPE,
			stderr=asyncio.subprocess.DEVNULL)
	print("subprocess started")
	# Read the "alive" message
	print((await sim_calc.stdout.readline()).decode('utf-8').strip())
	# Read the "ready" message
	print((await sim_calc.stdout.readline()).decode('utf-8').strip())

	asyncio.create_task(recv_sim_calc())
	await lc.start(token)

lc.loop.run_until_complete(main())
