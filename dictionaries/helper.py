import json, pickle
from typing import List, Dict, Any

_end = '_end_'

def build_trie(words):
    trie: Dict[str, Any] = dict()
    for word in words:
        current_dict = trie
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return trie

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
with open('./raw/words.json') as f:
    global_word_list: List[str] = json.load(f)

    # convert this to a trie for quick lookups
    trie = build_trie(global_word_list)

    with open('./ct_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./ct_words.pickle', 'wb') as handle:
        pickle.dump(global_word_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./raw/wlist_match2.txt') as f:
    words = [word.rstrip() for word in f.readlines()]
    # Do some cleanup
    words = [word for word in words if word.isalpha() and len(word) >= 4]

    trie = build_trie(words)

    with open('./w2_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./w2_words.pickle', 'wb') as handle:
        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('./raw/wlist_match12.txt') as f:
    words = [word.rstrip() for word in f.readlines()]
    # Do some cleanup
    words = [word for word in words if word.isalpha() and len(word) >= 4]

    trie = build_trie(words)

    with open('./w12_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)
    with open('./w12_words.pickle', 'wb') as handle:
        pickle.dump(words, handle, protocol=pickle.HIGHEST_PROTOCOL)
