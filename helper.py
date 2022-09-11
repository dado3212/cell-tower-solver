import json, pickle
from typing import List, Dict, Any

_end = '_end_'

def make_trie(words: List[str]) -> Dict[str, Any]:
    root: Dict[str, Any] = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return root

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
with open('words.json') as f:
    global_word_list: List[str] = json.load(f)

    # convert this to a trie for quick lookups
    trie = make_trie(global_word_list)

    with open('word_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)
