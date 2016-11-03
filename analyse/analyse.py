import json
import re
import string
from itertools import chain
from pprint import pprint

import nltk


IGNORE = ['а', 'на', 'с', 'году', 'и', 'в', 'для', 'это', 'также', 'не', 'от', 'ее',
'по', 'она', 'лет', 'как', 'из', 'под', 'после', 'за', 'со', 'у', 'что', 'уже', 'к', 'до', 'но', 
'его', 'так', 'где']

def preprocess(data): 
	cleaned = {}

	regex = re.compile('[%s«»–“”]' % re.escape(string.punctuation))

	for brand, about in data.items():
		lines = []

		for line in about: 
			line = line.replace('\n', '').replace('\r', '')

			if len(line) != 0: 
				lines.append(line)

		joined = ' '.join(lines)
		joined = regex.sub('', joined)

		cleaned[brand] = joined

	return cleaned

def words(data): 
	words = {}

	for brand, about in data.items():
		splited = about.split(' ')

		words[brand] = []

		for item in splited: 
			if len(item) != 0: 
				words[brand].append(item.lower())

	return words

def get_freq_dict(data):
	res = {} 

	for brand, words in data.items(): 
		res[brand] = nltk.FreqDist(words)

	return res

if __name__ == '__main__': 
	with open('about.json') as f: 
		data = json.load(f)

	processed = preprocess(data)
	words = words(processed)

	all_words = list(chain(*[v for k,v in words.items()]))

	# print(all_words)

	freq = [(k, v) for k, v in nltk.FreqDist(all_words).items() if not k in IGNORE]

	freq = sorted(freq, key=lambda item: item[1])

	K = 0.1

	pprint(freq[-int(K*len(freq)):])	