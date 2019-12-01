#!/usr/bin/env python3.7

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import sys
import json

embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder/3")

sess = tf.compat.v1.Session()
sess.run(tf.compat.v1.global_variables_initializer())
sess.run(tf.compat.v1.tables_initializer())

print("Tensorflow ready")

def find_matches(title, titles):
	titles.append(title)
	vecs = embed(titles)["outputs"].eval(session=sess)
	matches = list()
	near_matches = list()
	for i in range(len(vecs) - 1):
		similarity = np.inner(vecs[i], vecs[-1])
		if similarity > .9:
			matches.append(titles[i])
		elif similarity > .5:
			near_matches.append(titles[i])
	return {"matches": matches, "near_matches": near_matches}

for line in sys.stdin:
	req = json.loads(line)
	print(json.dumps(find_matches(req["title"], req["titles"])))
