#!/usr/bin/env python3.7

import sys
import discord
import asyncio
import re
import site_2D_Market
import site_Fakku
import site_Project_Hentai
import json
import traceback
import magazine_check
import romkan


site_modules = [site_2D_Market, site_Fakku, site_Project_Hentai]

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
	msg = await channel.send(embed=discord.Embed(
		title=f"Checking {site.name}",
		description="Fetching titles...",
		color=0x000000))
	try:
		titles = await site.get_manga_by_author(author)
		await msg.edit(embed=discord.Embed(
			title=f"Checking {site.name}",
			description="Comparing titles...",
			color=0x000000))
		pending_msgs[msg.id] = {"message": msg, "site": site.name}
		req = {"title": title, "titles": titles, "message_id": msg.id}
		sim_calc.stdin.write((json.dumps(req) + '\n').encode('utf-8'))
	except Exception as e:
		traceback.print_exc()
		if str(e):
			status = f'{type(e).__name__} - {e}'
		else:
			status = type(e).__name__
		await msg.edit(content=f"{site.name}: {status.strip()}")


@lc.event
async def on_message(msg):
	content = msg.content.strip().replace('“', '"').replace('”', '"')
	if not re.match(r"\.lc(:?\s+.*)?$", content):
		return

	author = None
	title = None
	link = None
	en = None

	# Handle EN/JP prior to regex matching
	if " -en" in content:
		en = True
		content = content.replace(" -en", "").strip()
	elif " -jp" in content:
		en = False
		content = content.replace(" -jp", "").strip()
	else:
		# default to English
		en = True

	# Regex matching for flags with arguments
	match1 = re.match(r'\.lc\s+"([^"]+)"\s+"([^"]+)"\s+"([^"]+)"$', content)
	match2 = re.match(r"\.lc\s+-(.)\s+(.+)\s+-(.)\s+(.+)\s+-(.)\s+(.+)$", content)
	if match1:
		author = match1.group(1)
		title = match1.group(2)
		link = match1.group(3)
	elif match2:
		for i in range(1, 6, 2):
			if match2.group(i) == 'a':
				author = match2.group(i + 1).strip().strip('"')
			elif match2.group(i) == 't':
				title = match2.group(i + 1).strip().strip('"')
			elif match2.group(i) == 'l':
				link = match2.group(i + 1).strip().strip('"')

	if author is None or len(author) == 0 or title is None or len(title) == 0 or link is None or len(link) == 0:
		asyncio.create_task(
			msg.channel.send('Invalid command. Usage: `.lc "author" "title" "link" (-en | -jp)` or `.lc -a author -t '
							 'title -l link (-en | -jp)`'))
		return

	# Run the licensed magazine check (only for nhentai)
	if "nhentai.net/g/" in link:
		licensed = await magazine_check.check_link(link)
		if licensed is not None:
			await msg.channel.send(embed=discord.Embed(
									title="**This doujin is most likely licensed.**",
									description=f"It appeared in the licensed magazine issue `{licensed}`.",
									color=0x000000))

	# Handle all JP text conversion here
	if not en:
		if "nhentai.net/g/" in link:
			await msg.channel.send("-jp flag detected. Parsing Japanese title...")
			title = await magazine_check.get_title_japanese(link)
		else:
			await msg.channel.send("-jp flag detected. Translating title to Hiragana...")
			title = romkan.to_hiragana(title)

	await msg.channel.send(f"Looking up {title} by {author}.")
	for site in site_modules:
		asyncio.create_task(process_site(site, author, title, msg.channel))
	# if not en:
	# 	await msg.channel.send(f"Looking up {jptitle} by {author}.")
	#	for site in site_modules:
	#		asyncio.create_task(process_site(site, author, jptitle, msg.channel))


async def recv_sim_calc():
	global pending_msgs
	while True:
		line = await sim_calc.stdout.readline()
		results = json.loads(line)
		msg_id = results["message_id"]
		del results["message_id"]
		m = pending_msgs[msg_id]
		del pending_msgs[msg_id]
		msg = m["message"]
		site = m["site"]

		matches = results["matches"]
		near_matches = results["near_matches"]
		fringe_matches = results["fringe_matches"]

		embed = discord.Embed(
			title=f"{site} Results",
			color=0x000000)

		v_matches = '\n'.join(matches)
		if v_matches == '':
			v_matches = 'None'
		embed.add_field(
			name="Matches",
			value=v_matches,
			inline=False)

		v_near = '\n'.join(near_matches)
		if v_near == '':
			v_near = 'None'
		embed.add_field(
			name="Near Matches",
			value=v_near,
			inline=False)

		v_fringe = '\n'.join(fringe_matches)
		if v_fringe == '':
			v_fringe = 'None'
		embed.add_field(
			name="Fringe Matches",
			value=v_fringe,
			inline=False)

		await msg.edit(embed=embed)


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
