import json

current_grid = [
    ['p','b','e','t','w','e','p'],
    ['a','r','t','e','n','r','o'],
    ['i','d','a','l','m','i','s'],
    ['l','r','a','w','t','e','d'],
    ['e','a','d','h','i','r','g'],
    ['i','n','h','a','d','r','o'],
    ['a','g','i','r','w','o','u'],
    ['f','b','l','o','r','k','p'],
    ['f','o','w','s','u','e','m'],
    ['l','r','d','w','p','d','e'],
    ['e','e','e','k','p','o','s'],
    ['g','a','l','r','t','s','y']
]

# Get all of the potential shapes
def valid_shapes(min_length, max_length):
    return []

_end = '_end_'

def make_trie(words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return root

def in_trie(trie, word):
    current_dict = trie
    for letter in word:
        if letter not in current_dict:
            return False
        current_dict = current_dict[letter]
    return _end in current_dict

with open('words.json') as f:
    words = json.load(f)
    max_length = max([len(x) for x in words]) # 8
    min_length = min([len(x) for x in words]) # 4

    # convert this to a trie for quick lookups
    trie = make_trie(words)
    # print(in_trie(trie, 'aardvark'))
    # print(in_trie(trie, 'pbest'))

def find_valid_words(grid, r, c):
    word = grid[r][c]
    # Technically you can go in any four digits, but because we're
    # Choosing the starting letter you can really only go right or down

    print(grid[r][c])

def solve(grid):
    # find words
    print(len(words))
    print(max_length)
    print(min_length)

    # give it a grid position. For now, let's start with 0, 0.
    print(find_valid_words(grid, 0, 0))

solve(current_grid)

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
