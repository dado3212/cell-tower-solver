from typing import List, Tuple
from Colors import nthSunflowerColor, printColor
from Shape import Shape
from Types import Square
from Types import Square

class Grid:
    def __init__(this, width: int, height: int, minSize: int, maxSize: int, characters: List[List[str]] = []):
        this.width = width
        this.height = height
        this.minSize = minSize
        this.maxSize = maxSize
        this.characters = None
        # Simple validations
        if len(characters) != 0:
            if len(characters[0]) != width:
                raise ValueError('Width appears to be wrong')
            if len(characters) != height:
                raise ValueError('Height appears to be wrong')
            this.characters = characters

    def squares(this) -> List[Square]:
        squares = []
        for r in range(this.height):
            for c in range(this.width):
                squares.append((r, c))
        return squares

    def getAdjacentSquares(this, square: Square) -> List[Square]:
        up = (square[0] - 1, square[1])
        right = (square[0], square[1] + 1)
        down = (square[0] + 1, square[1])
        left = (square[0], square[1] - 1)

        basic_squares = []
        for possible in [up, right, down, left]:
            if (possible[0] >= 0 and possible[0] < this.height and possible[1] >= 0 and possible[1] < this.width):
                basic_squares.append(possible)
        return basic_squares

    def setCharacters(this, characters: List[List[str]]) -> None:
        this.characters = characters

    def getCharacter(this, row: int, col: int) -> str:
        if this.characters is None:
            return ''
        return this.characters[row][col]

    def getWord(this, shape: Shape) -> str:
        if this.characters is None:
            raise ValueError('No characters are set, a word has no meaning')
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
