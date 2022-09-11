import json, pickle
from typing import List, Dict, Any

_end = '_end_'

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
with open('words.json') as f:
    global_word_list: List[str] = json.load(f)

    # convert this to a trie for quick lookups
    trie: Dict[str, Any] = dict()
    for word in global_word_list:
        current_dict = trie
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end

    with open('word_trie.pickle', 'wb') as handle:
        pickle.dump(trie, handle, protocol=pickle.HIGHEST_PROTOCOL)
