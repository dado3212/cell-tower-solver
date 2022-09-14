import json, pickle
from typing import List, Dict, Any

_end = '_end_'

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
