#!/usr/bin/env python3.7

import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

embed = hub.KerasLayer("https://tfhub.dev/google/universal-sentence-encoder/3")

print("Tensorflow ready")

session = tf.compat.v1.Session()
session.run(tf.compat.v1.global_variables_initializer())
session.run(tf.compat.v1.tables_initializer())

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
	outputs = embed(sentences)["outputs"]
	print(outputs.eval(session=session))

	'''
	print("Testing similarities...")
	print("Below should be three matches (closer to 1), "
			"followed by three non-matches (closer to 0).")
	print(compute_similarity(sentences[0], sentences[1]))
	print(compute_similarity(sentences[2], sentences[3]))
	print(compute_similarity(sentences[4], sentences[5]))
	print(compute_similarity(sentences[1], sentences[3]))
	print(compute_similarity(sentences[3], sentences[4]))
	print(compute_similarity(sentences[2], sentences[5]))
	'''
