from Shape import Shape
from typing import List, Dict, Optional, Tuple
import random, math
from Grid import Grid, easyGrid
from Utils import is_number_composable
from Solver import solve
from Words import global_word_list, is_word_composable, is_valid_word
from Types import Square

def createUniqueFromEmptyGrid(grid: Grid) -> Tuple[Grid, List[Shape]]:
    if not is_number_composable(len(grid.squares), grid.minSize, grid.maxSize):
        raise ValueError('You cannot build a grid of size %d with blocks sized between %d and %d', len(this.squares), minSize, maxSize)

    shapes: List[Shape] = []
    is_valid = False
    while not is_valid:
        shapes = buildShapePatternHelper(grid)
        grid.printShapes(shapes)
        is_valid = True
        built_grid = build(grid, shapes, True)
        if built_grid is None:
            print("No grid")
            is_valid = False
    print(built_grid)

    return (built_grid, shapes)

# Given the dimensions of a grid, and the possible tile sizes, this will attempt
# to return a set of Shapes that fully cover the grid
def buildShapePattern(grid: Grid) -> List[Shape]:
    if not is_number_composable(len(grid.squares), grid.minSize, grid.maxSize):
        raise ValueError('You cannot build a grid of size %d with blocks sized between %d and %d', len(this.squares), minSize, maxSize)

    shapes: List[Shape] = []
    is_valid = False
    while not is_valid:
        shapes = buildShapePatternHelper(grid)
        grid.printShapes(shapes)
        is_valid = True
        built_grid = build(grid, shapes, True)
        if built_grid is None:
            print("No grid")
            is_valid = False

    return shapes

def total_empty_shapes(grid: Grid, shape_mapping: Dict[Square, Optional[Shape]]) -> List[Shape]:
    empty_shape_mapping: Dict[Square, int] = dict()
    for square in shape_mapping:
        empty_shape_mapping[square] = 0
    squareCount = 1

    same: Dict[int, int] = dict()

    for square in grid.orderedSquares():
        # It's empty
        if shape_mapping[square] is None:
            # Check if any of the adjacents have numbers
            adjacent = grid.getAdjacentSquares(square)
            touching = []
            for adj in adjacent:
                if empty_shape_mapping[adj] != 0:
                    touching.append(empty_shape_mapping[adj])
            touching = list(set(touching))
            touching.sort()
            if len(touching) == 0:
                empty_shape_mapping[square] = squareCount
                squareCount += 1
            elif len(touching) == 1:
                empty_shape_mapping[square] = touching[0]
            else:
                empty_shape_mapping[square] = touching[0]
                for i in range(1, len(touching)):
                    t = touching[i]
                    if t not in same:
                        choosing = touching[0]
                        if choosing in same:
                            same[t] = same[choosing]
                        else:
                            same[t] = choosing
                    else:
                        same[t] = min(same[t], t)
    # Relax same
    same_keys = list(same.keys())
    same_keys.sort()
    for key in same_keys:
        maps = same[key]
        if maps in same:
            same[key] = same[maps]

    # Build shapes
    squares: Dict[int, List[Square]] = dict()
    for square in grid.orderedSquares():
        shapeCount = empty_shape_mapping[square]
        if shapeCount != 0:
            if shapeCount in same:
                shapeCount = same[shapeCount]
            if shapeCount in squares:
                squares[shapeCount].append(square)
            else:
                squares[shapeCount] = [square]
    shapes = [Shape(squares[x]) for x in squares]

    return sorted(shapes, key=lambda s: s.size())

def is_done(grid: Grid, shape_mapping: Dict[Square, Optional[Shape]]) -> bool:
    for square in shape_mapping:
        shape = shape_mapping[square]
        if shape is None:
            return False
        if shape.size() < grid.minSize or shape.size() > grid.maxSize:
            return False

    return True

def buildShapePatternCut(grid: Grid, shapes: List[Shape], currentShape: Shape, shape_mapping: Dict[Square, Optional[Shape]]):
    shapes = shapes[::]
    shapes.append(currentShape)
    # Find all of the current empty spaces
    empty_shapes = total_empty_shapes(grid, shape_mapping)

    # For each one, try and recursively solve them
    answers = []
    # Speed up by trivially checking if any of them are the wrong size
    for empty_shape in empty_shapes:
        if not is_number_composable(len(empty_shape.squares), grid.minSize, grid.maxSize):
            return None
    for empty_shape in empty_shapes:
        new_grid = Grid(empty_shape.squares, grid.minSize, grid.maxSize)
        new_shape_mapping = dict()
        for square in new_grid.squares:
            new_shape_mapping[square] = None
        answer = buildShapePatternRecurse(new_grid, [], Shape([new_grid.squares[0]]), new_shape_mapping)
        if answer is None:
            return None
        else:
            answers.append(answer)
    result = shapes
    for answer in answers:
        result += answer
    return result

def buildShapePatternGrow(grid: Grid, shapes: List[Shape], currentShape: Shape, shape_mapping: Dict[Square, Optional[Shape]]):
    options = grid.getAdjacentShapeSquares(currentShape)
    options = [opt for opt in options if shape_mapping[opt] is None]
    random.shuffle(options)
    for option in options:
        new_shape = Shape(currentShape.squares + [option])
        new_shape_mapping = shape_mapping.copy()
        for square in new_shape.squares:
            new_shape_mapping[square] = new_shape
        result = buildShapePatternRecurse(grid, shapes, new_shape, new_shape_mapping)
        if (result is not None):
            return result
    return None

def buildShapePatternRecurse(grid: Grid, shapes: List[Shape], currentShape: Shape, shape_mapping: Dict[Square, Optional[Shape]]):
    # Temp debugging
    # x = shapes[::]
    # x.append(currentShape)
    # grid.printShapes(x)
    # print("")

    if is_done(grid, shape_mapping):
        shapes.append(currentShape)
        return shapes
    if not is_number_composable(len(grid.squares), grid.minSize, grid.maxSize):
        return None
    if currentShape.size() == grid.maxSize:
        return buildShapePatternCut(grid, shapes, currentShape, shape_mapping)
    if currentShape.size() >= grid.minSize:
        grow_to_sizes = list(range(grid.minSize, grid.maxSize + 1))
        random.shuffle(grow_to_sizes)
        for grow_to in grow_to_sizes:
            if currentShape.size() == grow_to:
                return buildShapePatternCut(grid, shapes, currentShape, shape_mapping)
            else:
                return buildShapePatternGrow(grid, shapes, currentShape, shape_mapping)
    else:
        return buildShapePatternGrow(grid, shapes, currentShape, shape_mapping)

def buildShapePatternHelper(grid: Grid) -> List[Shape]:
    # Build the empty shape mapping
    shape_mapping: Dict[Square, Optional[Shape]] = dict()
    for square in grid.squares:
        shape_mapping[square] = None

    shapes = buildShapePatternRecurse(grid, [], Shape([grid.squares[0]]), shape_mapping)
    sorted_shapes = []
    for shape in shapes:
        squares = shape.squares
        squares.sort()
        sorted_shapes.append(Shape(squares))

    return sorted_shapes

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

    squares = []
    characters = []
    minSize = 100000
    maxSize = -1
    for shape in mapping.keys():
        for i in range(0, len(shape.squares)):
            squares.append(shape.squares[i])
            characters.append(mapping[shape][i])
        minSize = min(minSize, shape.size())
        maxSize = max(maxSize, shape.size())

    grid = Grid(squares, minSize, maxSize, characters)
    # temporary debugging
    grid.printBlank()
    return grid

# For a list of shapes, this randomly pulls a set of matching length words
# from the eligible word list.
def getPossibleWords(grid: Grid, shapes: List[Shape]) -> List[str]:
    words_by_length = dict()
    for word in global_word_list:
        length = len(word)
        # We don't need words of other lengths
        if length < grid.minSize or length > grid.maxSize:
            continue

        # Composable words can't build a unique grid
        if is_word_composable(word, grid.minSize, grid.maxSize):
            continue

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
def build(grid: Grid, shapes: List[Shape], debug: bool = False) -> Optional[Grid]:
    # For now, just assume the list of shapes is well formed
    num_wordlists = 5
    for i in range(num_wordlists):
        words = getPossibleWords(grid, shapes)
        if debug:
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
                if debug:
                    print("Retrying")
            else:
                return grid

    return None
