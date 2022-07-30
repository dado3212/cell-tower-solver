from Solver import Solver

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

solver = Solver(current_grid)
solver.solveGrid()
solver.printSolution()
