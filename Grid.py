from typing import List, Tuple
from Colors import nthSunflowerColor, printColor
from Shape import Shape
from Types import Square
from Types import Square

def easyGrid(width: int, height: int, minSize: int, maxSize: int, characters: List[str] = []):
    squares = []
    for r in range(height):
        for c in range(width):
            squares.append((r, c))
    return Grid(squares, minSize, maxSize, characters)

def circleGrid(radius: int):
    squares = []
    for r in range(2 * radius + 1):
        for c in range(2 * radius + 2):
            if (r-radius)**2 + (c-radius)**2 <= radius**2:
                squares.append((r, c))
    return Grid(squares, 4, 4)

def triangleGrid(base: int, height: int):
    squares = []
    for r in range(height):
        for c in range(base):
            if c <= r:
                squares.append((r, c))
    return Grid(squares, 4, 4)

class Grid:

    def __init__(this, squares: List[Square], minSize: int, maxSize: int, characters: List[str] = []):
        this.squares = squares
        this.minSize = minSize
        this.maxSize = maxSize

        character_mapping = dict()
        if len(characters) != 0:
            if len(characters) != len(squares):
                raise ValueError('Characters size does not match grid size')
            for i in range(0, len(squares)):
                character_mapping[squares[i]] = characters[i]
        else:
            character_mapping = None
        this.characterMapping = character_mapping

        this.fastSquares = dict()
        for square in this.squares:
            this.fastSquares[square] = True

    def orderedSquares(this) -> List[Square]:
        return sorted(this.squares)

    def getAdjacentSquares(this, square: Square) -> List[Square]:
        up = (square[0] - 1, square[1])
        right = (square[0], square[1] + 1)
        down = (square[0] + 1, square[1])
        left = (square[0], square[1] - 1)

        real = []
        for pos in [up, right, down, left]:
            if pos in this.fastSquares:
                real.append(pos)
        return real

    def getAdjacentShapeSquares(this, shape: Shape) -> List[Square]:
        adjacent_squares = dict()
        for square in shape.squares:
            up = (square[0] - 1, square[1])
            right = (square[0], square[1] + 1)
            down = (square[0] + 1, square[1])
            left = (square[0], square[1] - 1)

            adjacent_squares[up] = True
            adjacent_squares[right] = True
            adjacent_squares[down] = True
            adjacent_squares[left] = True

        for square in shape.squares:
            adjacent_squares.pop(square, None)

        real = []
        for square in adjacent_squares:
            if square in this.fastSquares:
                real.append(square)
        return real

    def setCharacters(this, characters: List[str]) -> None:
        character_mapping = dict()
        if len(characters) != len(this.squares):
            raise ValueError('Characters size does not match grid size')
        for i in range(0, len(this.squares)):
            character_mapping[this.squares[i]] = characters[i]
        this.characterMapping = character_mapping

    def getCharacter(this, square: Square) -> str:
        if this.characterMapping is None:
            return ' '
        return this.characterMapping[square]

    def getWord(this, shape: Shape) -> str:
        if this.characterMapping is None:
            raise ValueError('No characters are set, a word has no meaning')
        word = ""
        for square in shape.squares:
            word += this.getCharacter(square)
        return word

    def printBlank(this) -> None:
        maxHeight = 0
        maxWidth = 0
        for square in this.squares:
            maxHeight = max(square[0] + 1, maxHeight)
            maxWidth = max(square[1] + 1, maxWidth)
        for r in range(0, maxHeight):
            row = ""
            for c in range(0, maxWidth):
                if (r, c) not in this.squares:
                    row += '   '
                else:
                    row += ' ' + this.getCharacter((r, c)).upper() + ' '
            print(row)

    def printShapes(this, shapes: List[Shape]) -> None:
        i = 1
        for shape in shapes:
            shape.setColor(nthSunflowerColor(i))
            i += 6
        maxHeight = 0
        maxWidth = 0
        for square in this.squares:
            maxHeight = max(square[0] + 1, maxHeight)
            maxWidth = max(square[1] + 1, maxWidth)
        for r in range(0, maxHeight):
            row = ""
            for c in range(0, maxWidth):
                if (r, c) not in this.squares:
                    row += '   '
                else:
                    found_cell = False
                    for shape in shapes:
                        if (r, c) in shape.squares:
                            row += printColor(shape.getColor(), this.getCharacter((r, c)))
                            found_cell = True
                            break
                    if not found_cell:
                        row += ' _ '
            print(row)
