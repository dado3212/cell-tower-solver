from Words import max_length, is_valid_word

class Shape:
    def __eq__(self, other):
        return self.squares == other.squares

    # Squares is a list of points in lexical order
    def __init__(this, grid, potential_words, squares):
        this.grid = grid
        this.potential_words = potential_words
        this.squares = squares

    def getCurrentWord(this):
        word = ""
        for square in this.squares:
            word += this.grid[square[0]][square[1]]
        return word

    # static
    def cellIsValid(this, square):
        # Can't be out of bounds
        if (square[0] < 0 or square[0] >= len(this.grid) or square[1] < 0 or square[1] >= len(this.grid[0])):
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

    def getExpansionCells(this):
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

    def couldExpandToWord(this):
        if len(this.squares) == max_length:
            return is_valid_word(this.getCurrentWord())
        continuous_chunks = []
        last_square = None
        for square in this.squares:
            # Start it off
            if last_square is None:
                chunk = this.grid[square[0]][square[1]]
            elif last_square[0] == square[0] and last_square[1] + 1 == square[1]:
                chunk += this.grid[square[0]][square[1]]
            else:
                continuous_chunks.append(chunk)
                chunk = this.grid[square[0]][square[1]]
            last_square = square
        continuous_chunks.append(chunk)
        filtered_potential_words = []
        for word in this.potential_words:
            last_index = -1
            is_valid = True
            for chunk in continuous_chunks:
                if (last_index == -1):
                    i = word.find(chunk)
                else:
                    i = word.find(chunk, last_index)
                if i == -1:
                    is_valid = False
                    break
                last_index = i
            if is_valid:
                filtered_potential_words.append(word)
        this.potential_words = filtered_potential_words
        return len(filtered_potential_words) > 0

    def getExpandedShapes(this):
        cells = this.getExpansionCells()
        shapes = []
        for cell in cells:
            squares = [x for x in this.squares]
            squares.append(cell)
            squares.sort()
            new_shape = Shape(this.grid, this.potential_words, squares)
            if new_shape.couldExpandToWord():
                shapes.append(new_shape)
        return shapes

    def printShape(this):
        for r in range(0, len(this.grid)):
            row = ""
            for c in range(0, len(this.grid[r])):
                if (r, c) in this.squares:
                    row += this.grid[r][c]
                else:
                    row += '_'
            print(row)

    def setColor(this, color):
        this.color = color

    def getColor(this):
        return this.color
