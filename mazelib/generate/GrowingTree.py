
from mazelib.generate.MazeGenAlgo import MazeGenAlgo
from mazelib.generate.MazeGenAlgo import np
from random import choice, random, randrange


class GrowingTree(MazeGenAlgo):
    """
    The Algorithm

    1. Let C be a list of cells, initially empty. Add one cell to C, at random.
    2. Choose a cell from C, and carve a passage to any unvisited neighbor of that cell,
        adding that neighbor to C as well. If there are no unvisited neighbors,
        remove the cell from C.
    3. Repeat step 2 until C is empty.

    Optional Parameters

    backtrack_chance: float [0.0, 1.0]
        Splits the logic to either use Recursive Backtracking (RB) or Prim's (random)
        to select the next cell to visit. (default 1.0)
    """

    def __init__(self, w, h, backtrack_chance=1.0):
        super(GrowingTree, self).__init__(w, h)
        self.backtrack_chance = backtrack_chance

    def generate(self):
        # create empty grid
        a = np.empty((self.H, self.W), dtype=np.int8)
        a.fill(1)
        grid = a

        current_row, current_col = (randrange(1, self.H, 2), randrange(1, self.W, 2))
        grid[current_row][current_col] = 0
        active = self._find_neighbors(current_row, current_col, grid, True)
        active = [(current_row, current_col)]

        # continue until you have no more neighbors to move to
        while active:
            if random() < self.backtrack_chance:
                current_row, current_col = active[-1]
            else:
                current_row, current_col = choice(active)

            # find a visited neighbor
            next_neighbors = self._find_neighbors(current_row, current_col, grid, True)
            if len(next_neighbors) == 0:
                active = [a for a in active if a != (current_row, current_col)]
                continue

            nn_row, nn_col = choice(next_neighbors)
            active += [(nn_row, nn_col)]

            grid[nn_row][nn_col] = 0
            grid[(current_row + nn_row) // 2][(current_col + nn_col) // 2] = 0

        return grid
