from Solver import solve, find_words_for_seed
from Grid import Grid, easyGrid, circleGrid, triangleGrid
from Builder import build, buildGrid, shapeEccentricity, buildShapePattern, buildShapePatternHelper, createUniqueFromEmptyGrid
from Words import global_word_list

# ??
# current_grid = [
#     ['p','b','e','t','w','e','p'],
#     ['a','r','t','e','n','r','o'],
#     ['i','d','a','l','m','i','s'],
#     ['l','r','a','w','t','e','d'],
#     ['e','a','d','h','i','r','g'],
#     ['i','n','h','a','d','r','o'],
#     ['a','g','i','r','w','o','u'],
#     ['f','b','l','o','r','k','p'],
#     ['f','o','w','s','u','e','m'],
#     ['l','r','d','w','p','d','e'],
#     ['e','e','e','k','p','o','s'],
#     ['g','a','l','r','t','s','y']
# ]

# # 86
# grid = easyGrid(7, 12, 4, 8)
# grid.setCharacters(['n','e','i','p','r','o','g','a','t','h','e','r','e','o','g','r','a','b','s','s','p','e','s','l','u','p','t','i','i','d','e','s','e','b','o','e','n','p','e','t','e','n','t','i','f','r','i','t','s','y','m','e','o','d','t','e','l','a','n','o','v','r','a','i','i','n','g','e','l','b','n','s','r','a','l','l','u','k','p','o','u','n','d','m'])
# grid.printBlank()
# shapes = solve(grid)
# grid.printShapes(shapes)
# exit()

# Custom #1
# grid = easyGrid(14, 14, 4, 8, ['h','a','h','e','s','c','h','a','p','s','i','l','s','c','w','k','i','t','t','n','s','o','o','r','k','o','i','m','i','a','n','t','e','f','n','r','y','e','a','i','t','w','s','h','a','n','o','l','s','e','v','e','l','a','r','e','v','i','r','m','r','o','o','r','e','a','i','g','e','p','s','f','l','o','s','d','e','m','i','r','s','n','p','o','c','i','l','a','o','t','i','o','b','h','o','r','t','i','e','l','b','d','d','c','o','n','s','w','f','r','c','o','r','a','b','s','i','t','z','e','r','v','a','e','c','y','a','u','s','h','t','w','a','c','e','u','v','i','c','l','l','k','j','a','t','o','w','l','r','w','s','t','e','s','s','o','o','h','s','a','b','s','h','i','s','s','u','n','o','t','t','o','t','l','e','r','k','s','a','s','a','l','h','e','s','f','o','o','t','s','l','s','o','t','e','d'])
# grid.printBlank()
# shapes = solve(grid)
# grid.printShapes(shapes)
# exit()

# # 87
# old_grid = Grid([
#     ['d','i','w','a','t','b','a'],
#     ['g','i','t','r','r','n','k'],
#     ['n','u','n','s','a','p','t'],
#     ['m','o','f','f','h','i','r'],
#     ['b','i','c','e','r','i','d'],
#     ['u','n','h','m','p','r','o'],
#     ['a','w','e','l','v','e','s'],
#     ['d','a','p','i','n','d','t'],
#     ['e','r','e','g','h','a','y'],
#     ['t','e','c','o','i','k','s'],
#     ['c','t','n','g','h','i','n'],
#     ['s','f','u','s','e','d','g']
# ])

# # 102
# current_grid = Grid([
#     ['r','e','d','w','o','r','d'],
#     ['u','v','c','i','e','f','d'],
#     ['n','i','g','a','r','a','m'],
#     ['s','i','o','g','e','r','l'],
#     ['m','a','n','e','e','i','o'],
#     ['n','u','a','n','o','k','i'],
#     ['r','e','l','g','a','n','g'],
#     ['p','e','a','l','t','e','l'],
#     ['t','e','h','o','e','e','c'],
#     ['d','p','e','d','r','t','v'],
#     ['w','o','m','n','o','a','l'],
#     ['a','n','t','e','u','e','s']
# ])

# empty_grid = Grid([
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' '],
#     [' ',' ',' ',' ',' ',' ',' ']
# ])

# Normal pattern
# pattern = buildShapePattern(7, 12, 4, 8)
# grid = build(pattern)
# grid.printBlank()
# print()
# grid.printShapes(pattern)

# print()
# print()

# pattern_grid = circleGrid(5)
# print(len(pattern_grid.squares))
# characters = []
# for i in range(len(pattern_grid.squares)):
#     characters.append('-')
# pattern_grid.setCharacters(characters)
# pattern_grid.printBlank()
# exit()

# pattern_grid = triangleGrid(16, 16)
# print(len(pattern_grid.squares))
# characters = []
# for i in range(len(pattern_grid.squares)):
#     characters.append('-')
# pattern_grid.setCharacters(characters)
# pattern_grid.printBlank()
# pattern = buildShapePattern(pattern_grid)
# grid = build(pattern)
# print()
# grid.printShapes(pattern)
# exit()

# grid = triangleGrid(16, 16)
# characters = []
# grid.setCharacters(['h','a','l','e','m','a','t','r','b','o','a','s','g','d','c','c','t','a','s','a','s','c','s','s','g','a','h','g','o','n','p','f','l','b','a','s','t','u','b','l','l','u','w','h','a','s','t','a','i','z','z','k','s','d','c','g','l','k','t','l','t','e','p','a','p','z','l','o','h','a','a','z','s','a','s','r','a','l','w','r','t','p','e','h','n','g','u','f','c','e','v','y','d','e','a','o','s','a','t','p','f','k','g','a','p','u','e','d','n','s','t','t','y','a','c','e','s','t','e','d','k','s','m','a','r','e','r','i','m','e','r','e','e','y','e','s'])
# grid.printBlank()
# shapes = solve(grid)
# grid.printShapes(shapes)

# Very easy
#
# Above 22x22 we start hitting recursion depth problems
# when building the pattern.
# When doing >20x20 grids, (4, 8) struggles to find unique
# setups, likely due to the 4/8 relative primality
empty_grid = easyGrid(20, 20, 8, 8)
grid, shapes = createUniqueFromEmptyGrid(empty_grid)
grid.printBlank()
grid.printShapes(shapes)
exit()

# pattern_grid = easyGrid(8, 10, 5, 5)
# pattern = buildShapePattern(pattern_grid)
# grid = build(pattern)
# print()
# grid.printShapes(pattern)

# pattern = buildShapePattern(pattern_grid)
# grid = build(pattern)
# print()
# grid.printShapes(pattern)

# grid = Grid([(0, 0), (0, 1), (0, 2), (1, 0)], 4, 4)
# buildShapePatternHelper(grid)

# Larger pattern
# pattern = buildShapePattern(6, 10, 4, 4)
# grid = build(pattern)
# grid.printBlank()
# print()
# grid.printShapes(pattern)

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
