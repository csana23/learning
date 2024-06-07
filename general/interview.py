import nltk
from nltk.corpus import words

def get_all_words():
	nltk.download("words")
	return set(words.words())

def find_sentences(input_letters: str, all_words: set) -> list:
	"""
	Parameters
	----------
	input_letters: a string of letters a-z without spaces or punctuation
	all_words: the english dictionary. TODO: pick a type for this. task completed you stuck-up cuck
	Returns
	-------
	A list of possible sentences. A sentence is defined as a string of words separated by 
	spaces where each word is in all_words.  

	All letters in input_letters must appear in every output sentence in the same order as in the input.
	eg:
	find_sentences('aha', all_words) returns ['a ha', 'ah a', 'aha']
	find_sentences('helpisnowhere', all_words) returns ['help i snow here', 'help is now here', 
								'help is no where', 'help is nowhere']
	The last example does NOT include the following outputs:
	'help is now' -> wrong, doesn't include the last 4 letters from the input
	'help isnowhere' -> wrong, isnowhere is not a valid english word
	'help now here i snow' -> wrong, letters are in a different order to the input
	"""
	# okay now we have all english words
	# now we check which of these words are contained in the input_letters string
	# we need to create all possible divisions of the input string - this solves the problem of word ordering
	

    
