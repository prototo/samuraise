from nltk import sent_tokenize, word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords

from os.path import isfile
from re import sub

sample_text_file = 'sample_text'
punctuation = ',.;:\'!"[]{}()`?'
stop_words = stopwords.words()

def get_sentence_tokens(text):
	sent_tokens = sent_tokenize(text)
	return sent_tokens
	
def get_word_frequency(word_tokens):
	# get the most common words
	# TODO: amount depending on length of text
	frequency = FreqDist(word_tokens)
	most_common = frequency.most_common(len(word_tokens))

	length = sum([w[1] for w in most_common])
	tokens = {w[0]: {'freq':w[1], 'prob':w[1]/length} for w in most_common}

	# return the words without their counts
	return tokens

def get_word_tokens(text, get_most_frequent=True):
	# tokenise the text, removing punctuation and stopwords
	word_tokens = word_tokenize(strip_text(text))
	word_tokens = [w for w in word_tokens if w not in stop_words]
	return word_tokens

def strip_text(text):
	return sub('[^a-zA-Z\s\-]', '', text.lower())

def run(text):
	text = text.lower()
	sentences = get_sentence_tokens(text)
	text_tokens = get_word_tokens(text)
	text_frequency = get_word_frequency(text_tokens)
	weighted = []

	for index, sentence in enumerate(sentences):
		sentence_tokens = get_word_tokens(sentence)
		sentence_frequency = get_word_frequency(sentence_tokens)
		score = None
		for word in sentence_tokens:
			word_score = sentence_frequency[word].get('prop', 0)
			word_score += text_frequency[word].get('prob', 0)
			score = word_score if score==None else(score + word_score) / 2
		weighted.append((sentence, score, index))

	from math import floor
	divisor = 3
	# sort weighted by sentence probability
	weighted.sort(key=lambda tup: tup[1])
	cut_off = list(set([s[1] for s in weighted]))
	cut_off = cut_off[floor(len(cut_off)/divisor)]
	print('cut off', cut_off)

	# sort weighted by sentence index
	weighted.sort(key=lambda tup: tup[2])
	selected = [s[0] for s in weighted if s[1] >= cut_off]
	summary = ' '.join([s.capitalize() for s in selected])
	print(summary)
	print()
	print('summarised', len(sentences), 'sentences to', len(selected), 'sentences')

if __name__ == '__main__':
	# run the summarise method with the sample text file if it exists
	if isfile(sample_text_file):
		with open(sample_text_file) as f:
			run(f.read())
