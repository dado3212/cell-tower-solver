# Stuff that's used in Builder and Solver but I write bad code and so
# now it ends up here. I can clean this up later
from Grid import Grid
from Shape import Shape
from typing import List
from Types import Square
from Words import max_length, is_valid_word, chunk_matches_word

def squareIsValid(square: Square, width: int, height: int) -> bool:
    return (square[0] >= 0 and square[0] < height and square[1] >= 0 and square[1] < width)

def getExpansionCells(shape: Shape, width: int, height: int) -> List[Square]:
    basic_squares = []
    for square in shape.squares:
        up = (square[0] - 1, square[1])
        right = (square[0], square[1] + 1)
        down = (square[0] + 1, square[1])
        left = (square[0], square[1] - 1)
        for possible in [up, right, down, left]:
            if (possible not in basic_squares and squareIsValid(possible, width, height) and shape.cellIsClaimable(possible)):
                basic_squares.append(possible)
    # We should check some word validity here to prune bad options
    return basic_squares

def getExpandedShapes(grid: Grid, shape: Shape) -> List[Shape]:
    cells = getExpansionCells(shape, grid.width, grid.height)
    shapes = []
    for cell in cells:
        squares = [x for x in shape.squares]
        squares.append(cell)
        squares.sort()
        new_shape = Shape(shape.potential_words, squares)
        if couldExpandToWord(grid, new_shape):
            shapes.append(new_shape)
    return shapes


def couldExpandToWord(grid: Grid, shape: Shape) -> bool:
    if len(shape.squares) == max_length:
        return is_valid_word(grid.getWord(shape))
    continuous_chunks: List[str] = []
    last_square = None
    for square in shape.squares:
        # Start it off
        if last_square is None:
            chunk = grid.getCharacter(square[0], square[1])
        elif last_square[0] == square[0] and last_square[1] + 1 == square[1]:
            chunk += grid.getCharacter(square[0], square[1])
        else:
            continuous_chunks.append(chunk)
            chunk = grid.getCharacter(square[0], square[1])
        last_square = square
    continuous_chunks.append(chunk)
    filtered_potential_words = []
    for word in shape.potential_words:
        if chunk_matches_word(word, continuous_chunks):
            filtered_potential_words.append(word)
    shape.potential_words = filtered_potential_words
    return len(filtered_potential_words) > 0
