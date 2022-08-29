from typing import List, Tuple
from Colors import nthSunflowerColor, printColor
from Shape import Shape
from Types import Square

class Grid:
    # Squares is a list of points in lexical order
    def __init__(this, grid: List[List[str]]):
        this.grid = grid
        this.width: int = len(grid[0])
        this.height: int = len(grid)

    def getCharacter(this, row: int, col: int) -> str:
        return this.grid[row][col]

    def getWord(this, shape: Shape) -> str:
        word = ""
        for square in shape.squares:
            word += this.getCharacter(square[0], square[1])
        return word

    def printBlank(this) -> None:
        for r in range(0, this.height):
            row = ""
            for c in range(0, this.width):
                row += ' ' + this.getCharacter(r, c).upper() + ' '
            print(row)

    def printShapes(this, shapes: List[Shape]) -> None:
        i = 1
        for shape in shapes:
            shape.setColor(nthSunflowerColor(i))
            i += 6
        for r in range(0, this.height):
            row = ""
            for c in range(0, this.width):
                found_cell = False
                for shape in shapes:
                    if (r, c) in shape.squares:
                        row += printColor(shape.getColor(), this.getCharacter(r, c))
                        found_cell = True
                        break
                if not found_cell:
                    row += ' _ '
            print(row)
