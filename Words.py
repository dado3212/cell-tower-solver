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
    last_index = -1
    for chunk in chunks:
        if chunk not in word:
            return False
    for chunk in chunks:
        if (last_index == -1):
            i = word.find(chunk)
        else:
            i = word.find(chunk, last_index)
        if i == -1 or last_index == -1 and i > 0:
            return False
        last_index = i + len(chunk)
    return True

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
with open('words.json') as f:
    global_word_list: List[str] = json.load(f)

with open('word_trie.pickle', 'rb') as handle:
    trie = pickle.load(handle)
