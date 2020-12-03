#!/usr/bin/env python3.8

print("loading tensorflow", flush=True)

import tensorflow as tf
import tensorflow_hub as hub
import tensorflow_text
import numpy as np
import sys
import json

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-multilingual/3")

print("Tensorflow ready", flush=True)


def find_matches(title, titles):
	titles.append(title)
	vecs = embed(titles)  # ["outputs"].eval(session=sess)
	matches = list()
	near_matches = list()
	fringe_matches = list()
	for i in range(len(vecs) - 1):
		similarity = np.inner(vecs[i], vecs[-1])
		if similarity > .7:
			matches.append(titles[i])
		elif similarity > .4:
			near_matches.append(titles[i])
		elif similarity > .25:
			fringe_matches.append(titles[i])
	return {"matches": matches, "near_matches": near_matches, "fringe_matches": fringe_matches}


for line in sys.stdin:
	req = json.loads(line)
	output = find_matches(req["title"], req["titles"])
	output["message_id"] = req["message_id"]
	print(json.dumps(output), flush=True)
