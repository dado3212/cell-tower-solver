from Types import Square, Color
from typing import List
from Colors import printColor

class Shape:
    def __eq__(self, other):
        return self.squares == other.squares

    # Squares is a list of points in lexical order
    def __init__(this, potential_words: List[str], squares: List[Square]):
        this.potential_words = potential_words
        this.squares = squares

    # static
    def cellIsClaimable(this, square: Square) -> bool:
        # Can't be above the start square
        if (square[0] < this.squares[0][0]):
            return False
        # Can't be to the left of the start square if it's the same row
        if (square[0] == this.squares[0][0] and square[1] < this.squares[0][1]):
            return False
        # Can't already be part of the shape
        if (square in this.squares):
            return False
        return True

    def __str__(this) -> str:
        output = ""
        width = max([x[1] for x in this.squares])
        height = max([x[0] for x in this.squares])
        color_empty = (60, 60, 60, True)
        color_filled = (240, 240, 240, False)
        for r in range(0, height+1):
            row = ""
            for c in range(0, width+1):
                if (r, c) in this.squares:
                    row += printColor(color_filled, " ")
                else:
                    row += printColor(color_empty, " ")
            output += row + "\n"
        return output

    def setColor(this, color: Color) -> None:
        this.color = color

    def getColor(this) -> Color:
        return this.color
