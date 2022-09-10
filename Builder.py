from Shape import Shape
from typing import List, Dict, Optional, Tuple
import random, math
from Grid import Grid
from Solver import solve
from Words import global_word_list
from Types import Square
from Utils import squareIsValid, temp_print

# Given the dimensions of a grid, and the possible tile sizes, this will attempt
# to return a set of Shapes that fully cover the grid
def buildShapePattern(width: int, height: int, minSize: int, maxSize: int) -> List[Shape]:
    shapes: List[Shape] = []
    is_valid = False
    while not is_valid:
        shapes = buildShapePatternHelper(width, height, minSize, maxSize)
        temp_print(shapes, width, height)
        is_valid = True
        for x in shapes:
            if x.size() < minSize or x.size() > maxSize:
                print("Wrong sizing")
                is_valid = False
        if is_valid:
            temp_print(shapes, width, height)
            grid = build(shapes, True)
            if grid is None:
                print("No grid")
                is_valid = False

    return shapes

def altExpansionCells(shape: Shape, width: int, height: int) -> List[Square]:
    basic_squares = []
    for square in shape.squares:
        up = (square[0] - 1, square[1])
        right = (square[0], square[1] + 1)
        down = (square[0] + 1, square[1])
        left = (square[0], square[1] - 1)
        for possible in [up, right, down, left]:
            if (possible not in basic_squares and squareIsValid(possible, width, height) and possible not in shape.squares):
                basic_squares.append(possible)
    # We should check some word validity here to prune bad options
    return basic_squares

# Do some fixing. Really we should just build
# these correctly, but this is easier to wrap
# my head around. Don't expect this code to be
# long for this world
def fix_pass(shapes: List[Shape], width: int, height: int, minSize: int, maxSize: int) -> List[Shape]:
    # Get the number of shapes that are too small
    need_adjustment = [s for s in shapes if s.size() < minSize] # or s.size() > maxSize]

    # Check for the trivial case where we're good
    if len(need_adjustment) == 0:
        return shapes

    # Solve the first one, do this recursively
    to_fix = need_adjustment[0]

    adjacent_squares = altExpansionCells(to_fix, width, height)

    # x = [Shape([], [x]) for x in adjacent_squares]
    # x.append(to_fix)
    # temp_print(x, width, height)
    # exit()

    for adjacent_square in adjacent_squares:
        shape = [s for s in shapes if adjacent_square in s.squares][0]
        if shape.size() + to_fix.size() >= minSize and shape.size() + to_fix.size() <= maxSize:
            new_squares = shape.squares + to_fix.squares
            new_squares.sort()
            new_shape = Shape([], new_squares)
            new_shapes = [new_shape]
            for s in shapes:
                if s != to_fix and s != shape:
                    new_shapes.append(s)
            # exit()
            return fix_pass(new_shapes, width, height, minSize, maxSize)

    temp_print(shapes, width, height)
    print("WHOA")
    exit()
    return shapes

# [0, 1, 2, 3, 4, 5, 6, 7]

# Tuple of the square that will be joined, and the square that it will join
def select_square(square_options: Dict[Square, List[Square]], shape_mapping: Dict[Square, Optional[Shape]], minSize: int) -> Tuple[Square, Square]:
    print(square_options)
    # Check if any squares only have one option
    second_choice = dict()
    third_choice = dict()
    fourth_choice = []
    for square in square_options:
        options = square_options[square]
        if len(options) == 0:
            print("Ah shit, what did I do")
            exit()
        if len(options) == 1:
            return (square, options[0])
        else:
            # Check if it has shapes that are too small
            for opt in options:
                opt_shape = shape_mapping[opt]
                if opt_shape is not None and opt_shape.size() < minSize:
                    if opt_shape.size() in second_choice:
                        second_choice[opt_shape.size()].append((square, opt))
                    else:
                        second_choice[opt_shape.size()] = [(square, opt)]
                if opt_shape is not None:
                    if opt_shape.size() in third_choice:
                        third_choice[opt_shape.size()].append((square, opt))
                    else:
                        third_choice[opt_shape.size()] = [(square, opt)]
                fourth_choice.append((square, opt))
    # print(second_choice)
    # print(third_choice)
    # print(fourth_choice)
    if len(second_choice) > 0:
        # Pick the smallest group
        return random.choice(second_choice[min(second_choice.keys())])
    if len(third_choice) > 0:
        # Try and pick the smallest again?
        return random.choice(third_choice[min(third_choice.keys())])
    return random.choice(fourth_choice)

# Technically some of these grids will be valid, but not solvable.
# It's easier to just proceed until you can't, and then backtrack
# a little further.
# If we run into optimization problems we can make this a little
# more stringent.
def is_valid(grid: Grid, shape_mapping: Dict[Square, Optional[Shape]]) -> bool:
    # for each square in grid
    # check the neighbors
    has_empty_squares = False
    min_shape_size = grid.maxSize + 1
    for square in grid.squares():
        neighbors = grid.getAdjacentSquares(square)
        has_valid_neighbor = False
        for neighbor in neighbors:
            neighbor_shape = shape_mapping[neighbor]
            if neighbor_shape is None:
                has_valid_neighbor = True
            else:
                size = neighbor_shape.size()
                if (size < grid.maxSize):
                    has_valid_neighbor = True
        # test
        shape = shape_mapping[square]
        if shape is None:
            has_empty_squares = True
        else:
            min_shape_size = min(min_shape_size, shape.size())

        if not has_valid_neighbor:
            return False
    return has_empty_squares or min_shape_size >= grid.minSize

def buildShapePatternHelper(width: int, height: int, minSize: int, maxSize: int) -> List[Shape]:
    square_options: Dict[Square, List[Square]] = dict()
    shape_mapping: Dict[Square, Optional[Shape]] = dict()

    # Set up all_squares and square_options which we will use
    for r in range(height):
        for c in range(width):
            square = (r, c)
            shape_mapping[square] = None

            # Every square starts with a list of adjacent squares that it
            # can join. Because the grid starts with no shapes, we can
            # ignore the validity of these adjacent squares for now
            adjacent_squares: List[Square] = []
            # Up
            if (r > 0):
                adjacent_squares.append((r - 1, c))
            # Right
            if (c < width - 1):
                adjacent_squares.append((r, c + 1))
            # Down
            if (r < height - 1):
                adjacent_squares.append((r + 1, c))
            # Left
            if (c > 0):
                adjacent_squares.append((r, c - 1))

            square_options[square] = adjacent_squares

    # Proceed
    while (True):
        print("")
        if len(square_options) == 0:
            break
        # Pick a square
        selected = select_square(square_options, shape_mapping, minSize)
        print(selected)
        square = selected[0]
        joining = selected[1]

        shape = shape_mapping[joining]
        if (shape is None):
            # create a new shape with the two of them
            new_shape = Shape([], [square, joining])
            # add them to the shape mapping
            shape_mapping[square] = new_shape
            shape_mapping[joining] = new_shape
            # reduce the options
            del square_options[square]
            del square_options[joining]
        else:
            new_squares = shape.squares + [square]
            new_squares.sort()
            new_shape = Shape([], new_squares)
            for s in shape.squares:
                shape_mapping[s] = new_shape
            shape_mapping[square] = new_shape
            # reduce the options
            del square_options[square]

        # Clean up the options
        new_square_options: Dict[Square, List[Square]] = dict()
        for square in square_options:
            options = square_options[square]
            new_options = []
            for opt in options:
                shape = shape_mapping[opt]
                if shape is None:
                    new_options.append(opt)
                elif shape.size() < maxSize:
                    new_options.append(opt)
            new_square_options[square] = new_options
        square_options = new_square_options

    non_deduped_shapes = shape_mapping.values()
    shapes: List[Shape] = []
    for s in non_deduped_shapes:
        if s not in shapes:
            shapes.append(s)

    temp_print(shapes, width, height)

    return fix_pass(shapes, width, height, minSize, maxSize)

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
    width = max([shape.maxCol() for shape in mapping.keys()]) + 1
    height = max([shape.maxRow() for shape in mapping.keys()]) + 1

    raw_grid = []
    for _ in range(0, height):
        row = []
        for _ in range(0, width):
            row.append(' ')
        raw_grid.append(row)

    for shape in mapping.keys():
        for i in range(0, len(shape.squares)):
            raw_grid[shape.squares[i][0]][shape.squares[i][1]] = mapping[shape][i]

    return Grid(width, height, 4, 4, raw_grid)

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
def build(shapes: List[Shape], debug: bool = False) -> Optional[Grid]:
    # For now, just assume the list of shapes is well formed
    num_wordlists = 3
    for i in range(num_wordlists):
        words = getPossibleWords(shapes)
        if debug:
            print("Trying to build grid with words", words)
        mapping: Dict[str, List[Shape]] = dict()
        for word in words:
            mapping[word] = [shape for shape in shapes if len(word) == shape.size()]

        # The number of attempts with a given wordlist before we should just regenerate
        num_attempts = 5
        for i in range(num_attempts):
            new_mapping: Dict[Shape, str] = dict()
            for word in mapping:
                valid_shapes = [s for s in mapping[word] if s not in new_mapping]
                new_mapping[random.choice(valid_shapes)] = word

            grid = buildGrid(new_mapping)
            solution = solve(grid)
            if (solution == None):
                if debug:
                    print("Retrying")
            else:
                return grid

    return None
