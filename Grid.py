from typing import List

class Grid:
    # Squares is a list of points in lexical order
    def __init__(this, grid: List[List[str]]):
        this.grid = grid
        this.width: int = len(grid[0])
        this.height: int = len(grid)

    def getCharacter(this, row: int, col: int) -> str:
        return this.grid[row][col]
