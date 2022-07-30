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

# download valid wordlist used by the site
# https://www.andrewt.net/puzzles/cell-tower/assets/words.json
with open('words.json') as f:
    words = json.load(f)
    max_length = max([len(x) for x in words]) # 8
    min_length = min([len(x) for x in words]) # 4

    # convert this to a trie for quick lookups
    trie = make_trie(words)

class Colors:
    HEADERS = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

colors = [Colors.OKBLUE, Colors.OKCYAN, Colors.OKGREEN, Colors.WARNING, Colors.FAIL]

class Shape:

    def __eq__(self, other):
        return self.squares == other.squares

    # Squares is a list of points in lexical order
    def __init__(this, grid, potential_words, squares):
        this.grid = grid
        this.potential_words = potential_words
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

    def couldExpandToWord(this):
        if len(this.squares) == max_length:
            return in_trie(trie, this.getCurrentWord())
        # Bail out if it's relatively short
        if (len(this.squares) < 4):
            return True
        continuous_chunks = []
        last_square = None
        for square in this.squares:
            # Start it off
            if last_square is None:
                chunk = this.grid[square[0]][square[1]]
            elif last_square[0] == square[0] and last_square[1] + 1 == square[1]:
                chunk += this.grid[square[0]][square[1]]
            else:
                continuous_chunks.append(chunk)
                chunk = this.grid[square[0]][square[1]]
            last_square = square
        continuous_chunks.append(chunk)
        filtered_potential_words = []
        for word in this.potential_words:
            last_index = -1
            is_valid = True
            for chunk in continuous_chunks:
                i = word.find(chunk)
                if i == -1 or i < last_index:
                    is_valid = False
                    break
                last_index = i
            if is_valid:
                filtered_potential_words.append(word)
        this.potential_words = filtered_potential_words
        return len(filtered_potential_words) > 0

    def getExpandedShapes(this):
        cells = this.getExpansionCells()
        shapes = []
        for cell in cells:
            squares = [x for x in this.squares]
            squares.append(cell)
            squares.sort()
            new_shape = Shape(this.grid, this.potential_words, squares)
            if new_shape.couldExpandToWord():
                shapes.append(new_shape)
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

    def setColor(this, color):
        this.color = color

    def getColor(this):
        return this.color

# a = Shape(current_grid, (0, 0))
# seed = Shape(current_grid, [(1, 2)])
def find_words_for_seed(seed):
    seed = Shape(current_grid, words, [seed])
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
    valid_words = []
    valid_shapes = []
    for shape in all_shapes:
        word = shape.getCurrentWord()
        if word in words and word not in valid_words:
            valid_words.append(word)
            valid_shapes.append(shape)
    return (valid_words, valid_shapes)

def getKey(square):
    return str(square[0]) + '-' + str(square[1])

square_mapping = {}
for r in range(0, len(current_grid)):
    for c in range(0, len(current_grid[r])):
        square = (r, c)
        key = getKey(square)
        if key not in square_mapping:
            square_mapping[key] = []
        x = find_words_for_seed(square)
        valid_words = x[0]
        valid_shapes = x[1]
        for shape in valid_shapes:
            for square in shape.squares:
                key = getKey(square)
                if key in square_mapping:
                    square_mapping[key].append(shape)
                else:
                    square_mapping[key] = [shape]

# Dedupe step (there's a way to do this higher in the stack but I can't think right now)
for key in square_mapping:
    unique = []
    for shape in square_mapping[key]:
        if shape not in unique:
            unique.append(shape)
    square_mapping[key] = unique

# Try and deconstruct
# If any square is only reached by one cell, then it has to take that.
# Hopefully, that's sufficinet
def unique_square(sm):
    for key in sm:
        if len(sm[key]) == 1:
            return sm[key][0]
    return None

print("Built mapping")

solution = []
while True:
    unique = unique_square(square_mapping)
    if unique is None:
        break
    else:
        solution.append(unique)
        for square in unique.squares:
            filled_key = getKey(square)
            shapes_to_remove = square_mapping[filled_key]
            for shape_to_remove in shapes_to_remove:
                for square_to_clear in shape_to_remove.squares:
                    key_to_filter = getKey(square_to_clear)
                    square_mapping[key_to_filter] = [x for x in square_mapping[key_to_filter] if x != shape_to_remove]
            del square_mapping[filled_key]

def printShapes(solution, grid):
    i = 0
    for shape in solution:
        shape.setColor(colors[i])
        i = (i+1) % len(colors)

    for r in range(0, len(grid)):
        row = ""
        for c in range(0, len(grid[r])):
            found_cell = False
            for shape in solution:
                if (r, c) in shape.squares:
                    row += shape.getColor() + grid[r][c] + Colors.ENDC
                    found_cell = True
                    break
            if not found_cell:
                row += '_'
        print(row)

printShapes(solution, current_grid)
for pos in square_mapping:
    print(pos)
    for x in square_mapping[pos]:
        x.printShape()
