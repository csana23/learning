def find_sentences(input_letters: str, all_words: ?) -> List[str]:
	"""
	Parameters
	----------
	input_letters: a string of letters a-z without spaces or punctuation
	all_words: the english dictionary. TODO: pick a type for this
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
	# 1: iterate over the input string
    """
in_construction = ""
    list_of_individual_words = []

    for i in input_letters:
        in_construction += i

        if all_words.loc[all_words.word == in_construction] is not None:
            list_of_individual_words.append(in_construction)

            helplessnessisnowhere
    """
     list_of_individual_words = []

    for word in all_words:
        word in input_letters

        # extract this word
        list_of_individual_words.append()

    for j in input_letters:
        # remove the found word from the input string
        
        
    
