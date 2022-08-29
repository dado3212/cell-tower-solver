from Shape import Shape
from typing import List, Dict, Optional
import random, math
from Grid import Grid
from Solver import solve
from Words import global_word_list
from Types import Square

def temp_print(mapped_squares):
    non_deduped_shapes = mapped_squares.values()
    shapes: List[Shape] = []
    for s in non_deduped_shapes:
        if s not in shapes:
            shapes.append(s)

    empty_grid = Grid([
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' '],
        [' ',' ',' ',' ',' ',' ',' ']
    ])

    empty_grid.printShapes(shapes)
    print("")

# Given the dimensions of a grid, and the possible tile sizes, this will attempt
# to return a set of Shapes that fully cover the grid
def buildShapePattern(width: int, height: int, minSize: int, maxSize: int) -> List[Shape]:
    unfilled_squares: Dict[Square, bool] = dict()
    mapped_squares: Dict[Square, Shape] = dict()
    for r in range(height):
        for c in range(width):
            square = (r, c)
            unfilled_squares[square] = False

    min_colors = math.ceil(width * height / maxSize)
    max_colors = math.floor(width * height / minSize)
    starting_color_count = random.randint(min_colors, max_colors)

    while (len(unfilled_squares) > 0):
        # pick a random square
        random_square = random.sample(unfilled_squares.keys(), 1)[0]
        del unfilled_squares[random_square]

        print(random_square)

        # find an adjacent cell that is in bounds
        up = (random_square[0] - 1, random_square[1])
        right = (random_square[0], random_square[1] + 1)
        down = (random_square[0] + 1, random_square[1])
        left = (random_square[0], random_square[1] - 1)

        # too small
        too_small: List[Square] = []
        options: List[Square] = []
        for possible in [up, right, down, left]:
            # it must be in one of them
            if possible not in unfilled_squares and possible not in mapped_squares:
                continue

            if possible in mapped_squares and mapped_squares[possible].size() < minSize:
                too_small.append(possible)

            options.append(possible)

        # pick from the options
        # if one of the adjacent is length less than the min, then we add it
        if len(too_small) > 0:
            to_join = random.sample(too_small, 1)[0]
        else:
            to_join = random.sample(options, 1)[0]

        if to_join in unfilled_squares:
            del unfilled_squares[to_join]
            new_shape_squares = [to_join, random_square]
            new_shape_squares.sort()
            new_shape = Shape([], new_shape_squares)
            mapped_squares[to_join] = new_shape
            mapped_squares[random_square] = new_shape
        else:
            shape = mapped_squares[to_join]
            squares = shape.squares
            squares.append(random_square)
            squares.sort()
            shape.squares = squares
            mapped_squares[random_square] = shape

        # TEMPORARILY print it out
        # temp_print(mapped_squares)
        # join it with a random adjacent cell

    non_deduped_shapes = mapped_squares.values()
    shapes: List[Shape] = []
    for s in non_deduped_shapes:
        if s not in shapes:
            shapes.append(s)

    return shapes

# There is a notion of how good a tiled pattern is. My general heuristic is that
# larger chunks are better, and more curvy chunks are better.
# To start, I'm going to use
def shapeEccentricity(shapes: List[Shape]) -> float:
    num_shapes = 0
    total_size = 0
    total_sides = 0
    for shape in shapes:
        num_shapes += 1
        total_size += shape.size()
        total_sides += shape.numSides()
    return total_size * total_sides * 1.0 / (num_shapes ** 2)

# Takes in a mapping of shapes to words, and basically builds the empty grid in reverse
def buildGrid(mapping: Dict[Shape, str]) -> Grid:
    width = max([shape.maxCol() for shape in mapping.keys()])
    height = max([shape.maxRow() for shape in mapping.keys()])

    raw_grid = []
    for _ in range(0, height + 1):
        row = []
        for _ in range(0, width + 1):
            row.append(' ')
        raw_grid.append(row)

    for shape in mapping.keys():
        for i in range(0, len(shape.squares)):
            raw_grid[shape.squares[i][0]][shape.squares[i][1]] = mapping[shape][i]

    return Grid(raw_grid)

# For a list of shapes, this randomly pulls a set of matching length words
# from the eligible word list.
def getPossibleWords(shapes: List[Shape]) -> List[str]:
    words_by_length = dict()
    for word in global_word_list:
        length = len(word)
        if length in words_by_length:
            words_by_length[length].append(word)
        else:
            words_by_length[length] = [word]
    for length in words_by_length:
        words_to_shuffle = words_by_length[length]
        random.shuffle(words_to_shuffle)
        words_by_length[length] = words_to_shuffle

    needed = dict()
    for shape in shapes:
        length = shape.size()
        if length in needed:
            needed[length] += 1
        else:
            needed[length] = 1

    words = []
    for length in needed:
        for i in range(0, needed[length]):
            words.append(words_by_length[length][i])

    return words

# Takes in a pattern of shapes and tries to build a working grid
# There's a more elegant way to do random building, but this currently
# tends to work pretty well.
def build(shapes: List[Shape]) -> Optional[Grid]:
    # For now, just assume the list of shapes is well formed
    num_wordlists = 3
    for i in range(num_wordlists):
        words = getPossibleWords(shapes)
        print("Trying to build grid with words", words)
        mapping: Dict[str, List[Shape]] = dict()
        for word in words:
            mapping[word] = [shape for shape in shapes if len(word) == shape.size()]

        # The number of attempts with a given wordlist before we should just regenerate
        num_attempts = 10
        for i in range(num_attempts):
            new_mapping: Dict[Shape, str] = dict()
            for word in mapping:
                valid_shapes = [s for s in mapping[word] if s not in new_mapping]
                new_mapping[random.choice(valid_shapes)] = word

            grid = buildGrid(new_mapping)
            solution = solve(grid)
            if (solution == None):
                print("Retrying")
            else:
                return grid

    return None
