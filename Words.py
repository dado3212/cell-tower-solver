import json, pickle
from typing import List, Dict, Any

_end = '_end_'

# Currently only handles the 4/8 case
def is_word_composable(word: str, minSize: int, maxSize: int) -> bool:
    wordLength = len(word)
    if wordLength < minSize * 2:
        return False
    elif wordLength > maxSize:
        raise ValueError('This should never happen')
    else:
        for smallWordLength in range(minSize, int(wordLength / 2) + 1):
            # At the beginning
            if (is_valid_word(word[0:smallWordLength]) and is_valid_word(word[smallWordLength:])):
                return True
            # At the end (if it's different)
            if smallWordLength != wordLength/2:
                if (is_valid_word(word[-smallWordLength:]) and is_valid_word(word[:-smallWordLength])):
                    return True
    return False


def is_valid_word(word: str) -> bool:
    current_dict = trie
    for letter in word:
        if letter not in current_dict:
            return False
        current_dict = current_dict[letter]
    return _end in current_dict

def chunk_matches_word(word: str, chunks: List[str]) -> bool:
    # Quick and fast pass which filters a lot of options
    for chunk in chunks:
        if chunk not in word:
            return False
    # Acutally make sure the pieces fit
    last_index = -1
    for chunk in chunks:
        if (last_index == -1):
            i = word.find(chunk)
        else:
            i = word.find(chunk, last_index)
        if i == -1 or last_index == -1 and i > 0:
            return False
        last_index = i + len(chunk)
    return True

with open('dictionaries/w12_trie.pickle', 'rb') as handle:
    trie = pickle.load(handle)

with open('dictionaries/w12_words.pickle', 'rb') as handle:
    global_word_list = pickle.load(handle)
