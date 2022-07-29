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

class Shape:

    # Squares is a list of points in lexical order
    def __init__(this, grid, squares):
        this.grid = grid
        this.squares = squares

    def getCurrentWord(this):
        word = ""
        for square in this.squares:
            word += this.grid[square[0]][square[1]]
        return word

    # static
    def cellIsValid(this, square):
        # Can't already be claimed
        if (square in this.squares):
            return False
        # Can't be out of bounds
        if (square[0] < 0 or square[0] >= len(this.grid) or square[1] < 0 or square[1] >= len(this.grid[0])):
            return False
        # Can't be above the start square
        if (square[0] < this.squares[0][0]):
            return False
        # Can't be to the left of the start square if it's the same row
        if (square[0] == this.squares[0][0] and square[1] < this.squares[0][1]):
            return False
        return True

    def getExpansionCells(this):
        basic_squares = []
        for square in this.squares:
            up = (square[0] - 1, square[1])
            right = (square[0], square[1] + 1)
            down = (square[0] + 1, square[1])
            left = (square[0], square[1] - 1)
            for possible in [up, right, down, left]:
                if (possible not in basic_squares and this.cellIsValid(possible)):
                    basic_squares.append(possible)
        # We should check some word validity here to prune bad options
        return basic_squares

    def getExpandedShapes(this):
        cells = this.getExpansionCells()
        shapes = []
        for cell in cells:
            squares = [x for x in this.squares]
            squares.append(cell)
            squares.sort()
            shapes.append(Shape(this.grid, squares))
        return shapes

    def printShape(this):
        for r in range(0, len(this.grid)):
            row = ""
            for c in range(0, len(this.grid[r])):
                if (r, c) in this.squares:
                    row += this.grid[r][c]
                else:
                    row += '_'
            print(row)


# a = Shape(current_grid, (0, 0))
seed = Shape(current_grid, [(1, 2)])
shapes = [seed]
all_shapes = []
for i in range(0, 7):
    x = []
    for shape in shapes:
        new_shapes = shape.getExpandedShapes()
        x = x + new_shapes
    shapes = x
    if (i >= 2):
        all_shapes += x
all_shapes[-1].printShape()
all_shapes[0].printShape()

print(len(all_shapes))
# shape =
# print(shape.getCurrentWord())
# shapes = shape.getExpandedShapes()
# for shape in shapes:
#     new_shapes = shape.getExpandedShapes()
#     for s in new_shapes:
#         s.printShape()

# start at R*
# determine which cells are open to take
# for each cell check if the new shape is a valid word
# if it is, add the word and the new shape
# if it isn't, check if it's a possible word (regexes, insert .* on a line break)
# if it isn't, don't include it
# if it is, add it to the valid shapes
# continue up to a length of 8

# def valid_shapes(count):

#     print(count)

# def valid_shapes_length_one():
#     return [
#         [ (0, 0) ]
#     ]

# def valid_shapes_length_two():
#     return [
#         [ (0, 0), (0, 1) ],
#         [ (0, 0), (1, 0) ],
#     ]

# # Get all of the potential shapes of length 4 (to start)
# # ~86k total (heuristic)
# def generate_valid_shapes(length):
#     start = (0, 0)

#     # choose any direction, 4 times
#     # 1 -> 1
#     # 2 -> 2
#     # 3 -> 7
#     # 4 -> 2

#     # 2 -> 4 | 2 -> 2
#     # 3 -> 16 | 6 -> 2.6
#     # 4 -> 64 | 19 -> 3.36
#     # 5 -> 256
#     # 6 -> 1,024
#     # 7 -> 4,096
#     # 8 -> 16,384
#     shape = []
#     return []

# generate_valid_shapes(1)

# # def valid_shape_helper(start, min_length, max_length, valid_shapes, current_shape):
# #     for shape in valid_shapes:
# #         if len(shape) < max_length:
# #             left_r = shape[-1][0]
# #             left_c = shape[-1][1] - 1
# #             if ()
#     # go left
#     # go right
#     # go up
#     # go down


# _end = '_end_'

# def make_trie(words):
#     root = dict()
#     for word in words:
#         current_dict = root
#         for letter in word:
#             current_dict = current_dict.setdefault(letter, {})
#         current_dict[_end] = _end
#     return root

# def in_trie(trie, word):
#     current_dict = trie
#     for letter in word:
#         if letter not in current_dict:
#             return False
#         current_dict = current_dict[letter]
#     return _end in current_dict

with open('words.json') as f:
    words = json.load(f)
    # max_length = max([len(x) for x in words]) # 8
    # min_length = min([len(x) for x in words]) # 4

    # convert this to a trie for quick lookups
    # trie = make_trie(words)
    # print(in_trie(trie, 'aardvark'))
    # print(in_trie(trie, 'pbest'))

for shape in all_shapes:
    word = shape.getCurrentWord()
    if word in words:
        print(word)
        shape.printShape()

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
