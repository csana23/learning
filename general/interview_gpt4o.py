import nltk
from nltk.corpus import words
import itertools
from itertools import combinations

def get_all_words():
    nltk.download("words")
    all_words = set(words.words())

    for word in list(all_words):
        if len(word) == 1 and (word != "a" and word != "i"):
            all_words.remove(word)

    return all_words

def find_sentences(input_letters: str, all_words: set) -> list:
    def backtrack(remaining_letters, path):
        # If no remaining letters, we have completed a valid sentence
        if not remaining_letters:
            result.append(' '.join(path))
            return
        
        # Try every possible leading word
        for i in range(1, len(remaining_letters) + 1):
            word = remaining_letters[:i]
            if word in all_words:
                backtrack(remaining_letters[i:], path + [word])
    
    result = []
    backtrack(input_letters, [])
    return result



input_letters = "aha"
all_words = get_all_words()

print(
    find_sentences(input_letters=input_letters, all_words=all_words)
)