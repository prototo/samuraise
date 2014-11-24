from nltk import sent_tokenize, word_tokenize, bigrams, Text
from nltk.probability import FreqDist
from nltk.corpus import stopwords

from math import log, floor
from os.path import isfile, realpath, dirname
from os import walk, sep as separator
from re import sub
from sys import argv
import codecs

DIRNAME = dirname(realpath(__file__))

punctuation = ',.;:\'!"[]{}()`?'
stop_words = stopwords.words()

"""
	BACKGROUND CORPUS
"""
def get_background_corpus():
	corpus = {}
	corpus_location = separator.join((DIRNAME, 'corpus'))

	for dirpath, dirnames, filenames in walk(corpus_location):
		for filepath in filenames:
			filepath = separator.join((dirpath, filepath))
			with codecs.open(filepath, "r", "utf-8") as f:
				corpus[filepath] = f.read()
	return corpus

"""
	SENTENCES
"""
def get_sentence_tokens(text):
	sent_tokens = sent_tokenize(text)
	return sent_tokens

"""
	WORDS
"""
def get_word_tokens(text, without_stopwords=True):
	# tokenise the text, removing punctuation and stopwords
	word_tokens = word_tokenize(strip_text(text))
	if without_stopwords:
		word_tokens = [w for w in word_tokens if w not in stop_words]
	return word_tokens
	
def get_word_frequency(word_tokens):
	return FreqDist(word_tokens)

# get words with a minimum length of min_length
# if a frequency value is supplied, only words with a frequency greater or equal will be returned 
def get_long_words(tokens, min_lenth=10, frequency=None):
	words = [w for w in set(tokens) if len(w) >= min_lenth]
	if frequency:
		freqdist = get_word_frequency(tokens)
		words = [w for w in words if freqdist[w] >= frequency]
	return words

def get_collocations(tokens):
	text = Text(tokens)
	return text.collocations()

"""
	SAMPLE
"""
def strip_text(text):
	return sub('[^a-zA-Z\s\-]', '', text.lower())

"""
	ALGORITHMS
"""
def generate_tfidf(text, most_common=False):
	text = text.lower()
	tokens = get_word_tokens(text)
	tokens_freqdist = get_word_frequency(tokens)
	background_corpus = get_background_corpus()

	D = len(background_corpus)
	d = { w: 0 for w in tokens }
	for filepath, sample in background_corpus.items():
		sample_words = get_word_tokens(sample)
		sample_freqdist = get_word_frequency(sample_words)
		for word in tokens:
			if sample_freqdist[word] > 0:
				d[word] = 1
	tfidf = { word: (tokens_freqdist[word] * log(D/(1 + d[word]))) for word in tokens }

	if most_common and isinstance(most_common, int):
		return sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:most_common]

	return tfidf

def rank_sentences_tfidf(text, limit=10):
	text = text.lower()
	sentences = get_sentence_tokens(text)
	tokens = generate_tfidf(text).items()
	ranked = []

	for index, sentence in enumerate(sentences):
		score = 0
		stripped = strip_text(sentence)
		for token in tokens:
			if token[0] in stripped:
				score += token[1]
		ranked.append((index, sentence.capitalize(), score))

	l = len(ranked)
	for index, item in enumerate(ranked):
		average = item[2]
		if index > 0:
			average = (average + ranked[index - 1][2]) / 2
		if index < l - 1:
			average = (average + ranked[index + 1][2]) / 2
		# index, sentence, average surrounding score, score
		ranked[index] = (index, item[1], average, item[2])

	# sort ranked items by averaged surrounding score
	ranked.sort(key=lambda s: s[2], reverse=True)

	# return top X ranked sentences in appearance order
	return sorted(ranked[:limit], key=lambda x: x[0])

"""
	MAIN
"""
def run(text, quiet=True):
	keywords = [token[0] for token in sorted(generate_tfidf(text).items(), key=lambda x: x[1], reverse=True)][:10]
	ranked = rank_sentences_tfidf(text)
	summary = ' '.join([s[1] for s in ranked])

	if not quiet:
		print('keywords:', keywords)
		print('summary:', summary)
		print()
		print('summarised', len(text), 'chars to', len(summary), 'chars')

	return (keywords, summary)

if __name__ == '__main__':
	# if no file given exit script
	if len(argv) == 1:
		print('need a file to analyse')
		exit(1)

	sample_file = separator.join((DIRNAME, argv[1]))
	if not isfile(sample_file):
		print('given file does not exist')
		exit(2)

	print('reading', sample_file)
	# run the summarise method with the sample text file if it exists
	with open(sample_file) as f:
		run(f.read())
