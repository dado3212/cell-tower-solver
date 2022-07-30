import json

_end = '_end_'

def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return root

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
with open('words.json') as f:
    words = json.load(f)
    max_length = max([len(x) for x in words]) # 8
    min_length = min([len(x) for x in words]) # 4

    # convert this to a trie for quick lookups
    trie = make_trie(words)

def is_valid_word(word):
    current_dict = trie
    for letter in word:
        if letter not in current_dict:
            return False
        current_dict = current_dict[letter]
    return _end in current_dict

def chunk_matches_word(word, chunks):
    last_index = -1
    is_valid = True
    for chunk in chunks:
        if (last_index == -1):
            i = word.find(chunk)
        else:
            i = word.find(chunk, last_index)
        if i == -1 or last_index == -1 and i > 0:
            is_valid = False
            break
        last_index = i + len(chunk)
    return is_valid
