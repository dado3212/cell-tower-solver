from Shape import Shape
from typing import List, Dict, Optional, Tuple
import random, math, copy
from Grid import Grid, easyGrid
from Solver import solve
from Words import global_word_list
from Types import Square
from Utils import squareIsValid

# Given the dimensions of a grid, and the possible tile sizes, this will attempt
# to return a set of Shapes that fully cover the grid
def buildShapePattern(width: int, height: int, minSize: int, maxSize: int) -> List[Shape]:
    shapes: List[Shape] = []
    is_valid = False
    while not is_valid:
        grid = easyGrid(width, height, minSize, maxSize)
        shapes = buildShapePatternHelper(grid)
        # temp_print(shapes, width, height)
        is_valid = True
        for x in shapes:
            if x.size() < minSize or x.size() > maxSize:
                print("Wrong sizing")
                is_valid = False
        if is_valid:
            # temp_print(shapes, width, height)
            grid = build(shapes, True)
            if grid is None:
                print("No grid")
                is_valid = False

    return shapes

def total_empty_space(grid: Grid, square: Square, shape_mapping: Dict[Square, Optional[Shape]]) -> Shape:
    if shape_mapping[square] is not None:
        raise ValueError('This should only be called on empty')
    empty_shape = Shape([], [square])
    has_found = True
    while has_found:
        has_found = False
        adjacent = grid.getAdjacentShapeSquares(empty_shape)
        for pos in adjacent:
            if shape_mapping[pos] is None and pos not in empty_shape.squares:
                empty_shape = Shape([], empty_shape.squares + [pos])
                has_found = True
    return empty_shape

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
    for square in grid.squares:
        shape = shape_mapping[square]
        if shape is None:
            empty_shape = total_empty_space(grid, square, shape_mapping)
            if (empty_shape.size() < grid.minSize):
                adjacent = grid.getAdjacentShapeSquares(empty_shape)
                has_valid_adjacent = False
                for a in adjacent:
                    adjacent_shape = shape_mapping[a]
                    if adjacent_shape is not None and adjacent_shape.size() + empty_shape.size() <= grid.maxSize:
                        has_valid_adjacent = True
                if not has_valid_adjacent:
                    return False
            has_empty_squares = True
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
            if not has_valid_neighbor:
                return False
        else:
            min_shape_size = min(min_shape_size, shape.size())

    return has_empty_squares or min_shape_size >= grid.minSize

def is_done(grid: Grid, shape_mapping: Dict[Square, Optional[Shape]]) -> bool:
    for square in shape_mapping:
        shape = shape_mapping[square]
        if shape is None:
            return False
        if shape.size() < grid.minSize or shape.size() > grid.maxSize:
            return False

    # temporary printing
    for square in shape_mapping:
        shape = shape_mapping[square]
        print(shape.size())

    return True

def buildShapePatternRecurse(grid: Grid, shapes: List[Shape], currentShape: Shape, shape_mapping: Dict[Square, Optional[Shape]]):
    # temporary printing for debugging
    x = shapes[::]
    x.append(currentShape)
    grid.printShapes(x)
    print(len(shapes))

    if is_done(grid, shape_mapping):
        print("Is done")
        shapes.append(currentShape)
        return shapes
    if not is_valid(grid, shape_mapping):
        return None
    if currentShape.size() == grid.maxSize:
        # Pick a new place to start from
        shapes = shapes[::]
        shapes.append(currentShape)
        new_spot_options = []
        for square in shape_mapping:
            if shape_mapping[square] is None:
                new_spot_options.append(square)
        random.shuffle(new_spot_options)
        for spot in new_spot_options:
            new_shape = Shape([], [spot])
            new_shape_mapping = copy.deepcopy(shape_mapping)
            new_shape_mapping[spot] = new_shape
            result = buildShapePatternRecurse(grid, shapes, new_shape, new_shape_mapping)
            if (result is not None):
                return result
        return None
    else:
        # all choices
        options = grid.getAdjacentShapeSquares(currentShape)
        options = [opt for opt in options if shape_mapping[opt] is None]
        random.shuffle(options)
        for option in options:
            new_shape = Shape([], currentShape.squares + [option])
            new_shape_mapping = copy.deepcopy(shape_mapping)
            for square in new_shape.squares:
                new_shape_mapping[square] = new_shape
            result = buildShapePatternRecurse(grid, shapes, new_shape, new_shape_mapping)
            if (result is not None):
                return result
        return None

def buildShapePatternHelper(grid: Grid) -> List[Shape]:
    # Build the empty shape mapping
    shape_mapping: Dict[Square, Optional[Shape]] = dict()
    for square in grid.squares:
        shape_mapping[square] = None

    # And now we depth-first-search
    # for now we'll ignore that maxSize > minSize, and treat them as equal
    # Pseudocode
    # pick a random square
    # build a random shape of size minSize
    # at each growth point, check if the new grid is valid
    # if it's not, choose a different shape
    # if none of them are valid, back up
    # if none of them are valid, pick a new unfilled square

    # track this with a stack, where you can push on a square, and also a "end of shape" choice
    a = buildShapePatternRecurse(grid, [], Shape([], [(0, 0)]), shape_mapping)
    grid.printShapes(a)
    exit()
    return a

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

    return easyGrid(width, height, 4, 4, raw_grid)

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
