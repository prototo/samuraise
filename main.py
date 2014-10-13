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
	
def get_word_tokens(text):
	# tokenise the text, removing punctuation and stopwords
	word_tokens = word_tokenize(sub('[^\w\s]', '', text))
	word_tokens = [w for w in word_tokens if w not in stop_words]

	# get the most common words
	# TODO: amount depending on length of text
	frequency = FreqDist(word_tokens)
	most_common = frequency.most_common(10)

	# return the words without their counts
	return [w[0] for w in most_common]
	

def run(text):
	text_lower = text.lower()
	sent_tokens = get_sentence_tokens(text)
	word_tokens = get_word_tokens(text)

	# generate a list of the sentences with a count of how many word tokens appear in them
	summ_sentences = [[sentence, 0] for sentence in sent_tokens]
	for index in range(0, len(summ_sentences)):
		sentence = summ_sentences[index]
		for word in word_tokens:
			if word in sentence[0]:
				sentence[1] += 1

	# generate the summary text by dropping non common sentences
	common = [s[0] for s in summ_sentences if s[1]]
	summary = " ".join(common)

	print(summary)
	print()
	print('summarised', len(text), 'words to', len(summary), 'words')

if __name__ == '__main__':
	# run the summarise method with the sample text file if it exists
	if isfile(sample_text_file):
		with open(sample_text_file) as f:
			run(f.read())
