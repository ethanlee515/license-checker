#!/usr/bin/env python3.7

print("Loading Tensorflow...")
# IF using tensorflow 2.0+
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
# ELSE
# import tensorflow as tf
# ENDIF

import tensorflow_hub as hub
import numpy as np

print("Loading Tensorflow module...")
embed = hub.Module("https://tfhub.dev/google/universal-sentence-encoder/2")
print("Tensorflow module loaded")

session = tf.Session()
session.run(tf.global_variables_initializer())
session.run(tf.tables_initializer())

def compute_similarity(title1, title2):
	vecs = session.run(embed([title1, title2]))
	arrs = [np.array(vecs[i]) for i in (0, 1)]
	return np.inner(arrs[0], arrs[1])
	
if __name__ == "__main__":
	sentences = [
		"How old are you?",
		"What is your age?",
		"I like your phone.",
		"Your cellphone looks great.",
		"Hi, how is it going?",
		"How are you doing?"]
	print("Testing similarities...")
	print("Below should be three matches (closer to 1), "
			"followed by three non-matches (closer to 0).")
	print(compute_similarity(sentences[0], sentences[1]))
	print(compute_similarity(sentences[2], sentences[3]))
	print(compute_similarity(sentences[4], sentences[5]))
	print(compute_similarity(sentences[1], sentences[3]))
	print(compute_similarity(sentences[3], sentences[4]))
	print(compute_similarity(sentences[2], sentences[5]))
