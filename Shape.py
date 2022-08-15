from Words import max_length, is_valid_word, chunk_matches_word
from Grid import Grid
from typing import Tuple, List
from Colors import Color

Square = Tuple[int, int]

class Shape:
    def __eq__(self, other):
        return self.squares == other.squares

    # Squares is a list of points in lexical order
    def __init__(this, grid: Grid, potential_words: List[str], squares: List[Square]):
        this.grid = grid
        this.potential_words = potential_words
        this.squares = squares

    def getCurrentWord(this) -> str:
        word = ""
        for square in this.squares:
            word += this.grid.getCharacter(square[0], square[1])
        return word

    # static
    def cellIsValid(this, square: Square) -> bool:
        # Can't be out of bounds
        if (square[0] < 0 or square[0] >= this.grid.height or square[1] < 0 or square[1] >= this.grid.width):
            return False
        # Can't be above the start square
        if (square[0] < this.squares[0][0]):
            return False
        # Can't be to the left of the start square if it's the same row
        if (square[0] == this.squares[0][0] and square[1] < this.squares[0][1]):
            return False
        # Can't already be claimed
        if (square in this.squares):
            return False
        return True

    def getExpansionCells(this) -> List[Square]:
        basic_squares = []
        for square in this.squares:
            up = (square[0] - 1, square[1])
            right = (square[0], square[1] + 1)
            down = (square[0] + 1, square[1])
            left = (square[0], square[1] - 1)
            for possible in [up, right, down, left]:
                if (possible not in basic_squares and this.cellIsValid(possible)):
                    basic_squares.append(possible)
        # We should check some word validity here to prune bad options
        return basic_squares

    def couldExpandToWord(this) -> bool:
        if len(this.squares) == max_length:
            return is_valid_word(this.getCurrentWord())
        continuous_chunks: List[str] = []
        last_square = None
        for square in this.squares:
            # Start it off
            if last_square is None:
                chunk = this.grid.getCharacter(square[0], square[1])
            elif last_square[0] == square[0] and last_square[1] + 1 == square[1]:
                chunk += this.grid.getCharacter(square[0], square[1])
            else:
                continuous_chunks.append(chunk)
                chunk = this.grid.getCharacter(square[0], square[1])
            last_square = square
        continuous_chunks.append(chunk)
        filtered_potential_words = []
        for word in this.potential_words:
            if chunk_matches_word(word, continuous_chunks):
                filtered_potential_words.append(word)
        this.potential_words = filtered_potential_words
        return len(filtered_potential_words) > 0

    def __str__(this) -> str:
        output = ""
        for r in range(0, this.grid.height):
            row = ""
            for c in range(0, this.grid.width):
                if (r, c) in this.squares:
                    row += this.grid.getCharacter(r, c)
                else:
                    row += '_'
            output += row + "\n"
        return output

    def setColor(this, color: Color) -> None:
        this.color = color

    def getColor(this) -> Color:
        return this.color
