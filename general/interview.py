import nltk
from nltk.corpus import words
import itertools
from itertools import combinations

# helper functions
def get_all_words():
	nltk.download("words")
	return set(words.words())

def get_all_substrings(input: str):
    length = len(input) + 1
    division_list = [input[x:y] for x, y in combinations(range(length), r=2)]

    res = []
    [res.append(x) for x in division_list if x not in res]
    return res

def all_combinations(input_list: list):
    all_combinations_list = []
    for r in range(len(input_list) + 1):
        all_combinations_list.extend(itertools.combinations(input_list, r))
    return all_combinations_list

# end result
def find_sentences(input_letters: str, all_words: set) -> list:
	division_list = get_all_substrings(input_letters)

	division_dict =  {k: v for v, k in enumerate(division_list)}

	division_set = set(division_list)
	division_all_intersect = division_set.intersection(all_words)

	filtered_division_dict = {key: division_dict[key] for key in division_all_intersect}
	filtered_division_dict = {k: v for k, v in sorted(filtered_division_dict.items(), key=lambda item: item[1])}

	for word in list(filtered_division_dict):
		if len(word) == 1 and (word != "a" and word != "i"):
			filtered_division_dict.pop(word)

	filtered_division_list = list(filtered_division_dict.keys())

	combos = all_combinations(filtered_division_list)

	reference_input = [*input_letters]

	combos_joined = [("".join(tuples)).replace(" ", "") for tuples in combos]

	combos_joined_list = [[*x] for x in combos_joined]

	correct_indices = [index for index, value in enumerate(combos_joined_list) if value == reference_input]

	return [" ".join(combos[i]) for i in correct_indices]

input_letters = "aha"
all_words = get_all_words()

print(find_sentences(input_letters=input_letters, all_words=all_words))





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
    
