from Shape import Shape
from Words import words, is_valid_word
from Colors import nthSunflowerColor, printColor
import random

def getKey(square):
    return str(square[0]) + '-' + str(square[1])

# Try and deconstruct
# If any square is only reached by one cell, then it has to take that.
# Hopefully, that's sufficinet
def unique_square(sm):
    for key in sm:
        if len(sm[key]) == 1:
            return sm[key][0]
    return None

def remove_shape_from_map(sm, shape_to_remove):
    for square_to_clear in shape_to_remove.squares:
        key_to_filter = getKey(square_to_clear)
        sm[key_to_filter] = [x for x in sm[key_to_filter] if x != shape_to_remove]

def reduced_map(sm_orig, shape):
    sm = sm_orig.copy()
    for square in shape.squares:
        filled_key = getKey(square)
        shapes_to_remove = sm[filled_key]
        for shape_to_remove in shapes_to_remove:
            remove_shape_from_map(sm, shape_to_remove)
        del sm[filled_key]
    return sm

def has_solution(sm):
    for key in sm:
        if len(sm[key]) == 0:
            return False
    return True

class Solver:
    def __init__(this, grid):
        this.grid = grid

    def find_words_for_seed(this, seed):
        start = this.grid[seed[0]][seed[1]]
        xword = [x for x in words if x[0] == start]
        seed = Shape(this.grid, xword, [seed])
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
        valid_shapes = []
        for shape in all_shapes:
            word = shape.getCurrentWord()
            if is_valid_word(word) and shape not in valid_shapes:
                valid_shapes.append(shape)
        return valid_shapes

    def solveGrid(this):
        square_mapping = {}
        for r in range(0, len(this.grid)):
            for c in range(0, len(this.grid[r])):
                square = (r, c)
                key = getKey(square)
                square_mapping[key] = []

        for r in range(0, len(this.grid)):
            for c in range(0, len(this.grid[r])):
                square = (r, c)
                key = getKey(square)
                valid_shapes = this.find_words_for_seed(square)
                for shape in valid_shapes:
                    for square in shape.squares:
                        key = getKey(square)
                        square_mapping[key].append(shape)

        # Dedupe step (there's a way to do this higher in the stack but I can't think right now)
        for key in square_mapping:
            unique = []
            for shape in square_mapping[key]:
                if shape not in unique:
                    unique.append(shape)
            square_mapping[key] = unique

        # For debugging
        # print("Built mapping")
        # for key in square_mapping:
        #     print(key)
        #     print([x.getCurrentWord() for x in square_mapping[key]])

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
        this.solution = solution

    def printSolution(this):
        if this.solution is None:
            print("No solution found.")
        else:
            i = 1
            for shape in this.solution:
                shape.setColor(nthSunflowerColor(i))
                i += 6
            for r in range(0, len(this.grid)):
                row = ""
                for c in range(0, len(this.grid[r])):
                    found_cell = False
                    for shape in this.solution:
                        if (r, c) in shape.squares:
                            row += printColor(shape.getColor(), this.grid[r][c])
                            found_cell = True
                            break
                    if not found_cell:
                        row += '_'
                print(row)
