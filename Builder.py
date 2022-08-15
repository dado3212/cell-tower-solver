from Shape import Shape
from typing import List, Dict, Optional
import random
from Grid import Grid
from Solver import solve
from Words import global_word_list

# Given the dimensions of a grid, and the possible tile sizes, this will attempt
# to return a set of Shapes that fully cover the grid
def buildShapePattern(width: int, height: int, minSize: int, maxSize: int) -> List[Shape]:
    return []

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
