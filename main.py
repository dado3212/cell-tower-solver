from Solver import solve
from Grid import Grid
from Builder import build, buildGrid, shapeEccentricity, buildShapePattern

# ??
current_grid = [
    ['p','b','e','t','w','e','p'],
    ['a','r','t','e','n','r','o'],
    ['i','d','a','l','m','i','s'],
    ['l','r','a','w','t','e','d'],
    ['e','a','d','h','i','r','g'],
    ['i','n','h','a','d','r','o'],
    ['a','g','i','r','w','o','u'],
    ['f','b','l','o','r','k','p'],
    ['f','o','w','s','u','e','m'],
    ['l','r','d','w','p','d','e'],
    ['e','e','e','k','p','o','s'],
    ['g','a','l','r','t','s','y']
]

# 86
current_grid = [
    ['n','e','i','p','r','o','g'],
    ['a','t','h','e','r','e','o'],
    ['g','r','a','b','s','s','p'],
    ['e','s','l','u','p','t','i'],
    ['i','d','e','s','e','b','o'],
    ['e','n','p','e','t','e','n'],
    ['t','i','f','r','i','t','s'],
    ['y','m','e','o','d','t','e'],
    ['l','a','n','o','v','r','a'],
    ['i','i','n','g','e','l','b'],
    ['n','s','r','a','l','l','u'],
    ['k','p','o','u','n','d','m']
]

# 87
old_grid = Grid([
    ['d','i','w','a','t','b','a'],
    ['g','i','t','r','r','n','k'],
    ['n','u','n','s','a','p','t'],
    ['m','o','f','f','h','i','r'],
    ['b','i','c','e','r','i','d'],
    ['u','n','h','m','p','r','o'],
    ['a','w','e','l','v','e','s'],
    ['d','a','p','i','n','d','t'],
    ['e','r','e','g','h','a','y'],
    ['t','e','c','o','i','k','s'],
    ['c','t','n','g','h','i','n'],
    ['s','f','u','s','e','d','g']
])

# 102
current_grid = Grid([
    ['r','e','d','w','o','r','d'],
    ['u','v','c','i','e','f','d'],
    ['n','i','g','a','r','a','m'],
    ['s','i','o','g','e','r','l'],
    ['m','a','n','e','e','i','o'],
    ['n','u','a','n','o','k','i'],
    ['r','e','l','g','a','n','g'],
    ['p','e','a','l','t','e','l'],
    ['t','e','h','o','e','e','c'],
    ['d','p','e','d','r','t','v'],
    ['w','o','m','n','o','a','l'],
    ['a','n','t','e','u','e','s']
])

empty_grid = Grid([
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' '],
    [' ',' ',' ',' ',' ',' ',' ']
])

# Normal pattern
# pattern = buildShapePattern(7, 12, 4, 8)
# grid = build(pattern)
# grid.printBlank()
# print()
# grid.printShapes(pattern)

# print()
# print()

# Larger pattern
pattern = buildShapePattern(25, 25, 5, 8)
grid = build(pattern)
grid.printBlank()
print()
grid.printShapes(pattern)

# solution_old = solve(old_grid)
# old_grid.printShapes(solution_old)
# randomized_grid = build(solution_old)
# print(shapeEccentricity(solution_old))
# print()
# solution2 = solve(randomized_grid)
# randomized_grid.printShapes(solution2)
# print(shapeEccentricity(solution2))

# solution_current = solve(current_grid)
# current_grid.printShapes(solution_current)
# print(shapeEccentricity(solution_current))

# empty_grid.printShapes(solution_old)
