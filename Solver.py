from Shape import Shape
from Words import global_word_list, is_valid_word, chunk_matches_word
from Types import Square
from Grid import Grid
from typing import List, Dict, Optional

def getExpansionCells(grid: Grid, shape: Shape) -> List[Square]:
    basic_squares = []
    for square in grid.getAdjacentShapeSquares(shape):
        if shape.cellIsClaimable(square):
            basic_squares.append(square)
    # We should check some word validity here to prune bad options
    return basic_squares

def couldExpandToWord(grid: Grid, shape: Shape) -> bool:
    if len(shape.squares) == grid.maxSize:
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

def getExpandedShapes(grid: Grid, shape: Shape) -> List[Shape]:
    cells = getExpansionCells(grid, shape)
    shapes = []
    for cell in cells:
        squares = [x for x in shape.squares]
        squares.append(cell)
        squares.sort()
        new_shape = Shape(shape.potential_words, squares)
        if couldExpandToWord(grid, new_shape):
            shapes.append(new_shape)
    return shapes

# Try and deconstruct
# If any square is only reached by one cell, then it has to take that.
# Hopefully, that's sufficinet
def unique_square(sm: Dict[Square, List[Shape]]) -> Optional[Shape]:
    for key in sm:
        if len(sm[key]) == 1:
            return sm[key][0]
    return None

def remove_shape_from_map(sm: Dict[Square, List[Shape]], shape_to_remove: Shape) -> None:
    for square_to_clear in shape_to_remove.squares:
        sm[square_to_clear] = [x for x in sm[square_to_clear] if x != shape_to_remove]

def reduced_map(sm_orig: Dict[Square, List[Shape]], shape: Shape) -> Dict[Square, List[Shape]]:
    sm = sm_orig.copy()
    for square in shape.squares:
        shapes_to_remove = sm[square]
        for shape_to_remove in shapes_to_remove:
            remove_shape_from_map(sm, shape_to_remove)
        del sm[square]
    return sm

def has_solution(sm: Dict[str, List[Shape]]) -> bool:
    for key in sm:
        if len(sm[key]) == 0:
            return False
    return True

def find_words_for_seed(grid: Grid, seed: Square) -> List[Shape]:
    start = grid.getCharacter(seed[0], seed[1])
    xword = [x for x in global_word_list if x[0] == start]
    seed = Shape(xword, [seed])
    shapes = [seed]
    all_shapes = []
    for i in range(0, grid.maxSize):
        x = []
        for shape in shapes:
            new_shapes = getExpandedShapes(grid, shape)
            x = x + new_shapes
        shapes = x
        if (i >= grid.minSize - 2):
            all_shapes += x
    valid_shapes = []
    for shape in all_shapes:
        word = grid.getWord(shape)
        if is_valid_word(word) and shape not in valid_shapes:
            valid_shapes.append(shape)
    return valid_shapes

def solve(grid: Grid) -> Optional[List[Shape]]:
    square_mapping: Dict[Square, List[Shape]] = {}
    for square in grid.squares:
        square_mapping[square] = []

    for square in grid.squares:
        valid_shapes = find_words_for_seed(grid, square)
        for shape in valid_shapes:
            for sq in shape.squares:
                square_mapping[sq].append(shape)

    # Dedupe step (there's a way to do this higher in the stack but I can't think right now)
    for key in square_mapping:
        unique = []
        for shape in square_mapping[key]:
            if shape not in unique:
                unique.append(shape)
        square_mapping[key] = unique

    solution = []
    while True:
        unique = unique_square(square_mapping)
        if unique is None:
            # Try and find a word
            removed_something = False
            for key in square_mapping:
                for shape in square_mapping[key]:
                    if not has_solution(reduced_map(square_mapping, shape)):
                        remove_shape_from_map(square_mapping, shape)
                        removed_something = True
            if not removed_something:
                break
        else:
            solution.append(unique)
            square_mapping = reduced_map(square_mapping, unique)
    if len(square_mapping) == 0:
        return solution
    else:
        # Temp debugging
        # for k in square_mapping:
        #     print(k)
        #     for s in square_mapping[k]:
        #         print(grid.getWord(s))
        # print(solution)

        # Failed to find a solution
        return None
