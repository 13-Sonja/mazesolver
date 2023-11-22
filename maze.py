from cell import Cell
from time import sleep
import random


class Maze():
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)
        self._cells = []
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = [[Cell(self._win) for _ in range(self._num_rows)] for _ in range(self._num_cols)]
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._draw_cell(col, row)

    def _draw_cell(self, i, j):
        if not self._win:
            return
        cell_x1 = self._x1 + (i * self._cell_size_x)
        cell_y1 = self._y1 + (j * self._cell_size_y)
        cell_x2 = cell_x1 + self._cell_size_x
        cell_y2 = cell_y1 + self._cell_size_y
        self._cells[i][j].draw(cell_x1, cell_y1, cell_x2, cell_y2)
        self._animate(duration=0.01)

    def _animate(self, duration=0.06):
        self._win.redraw()
        sleep(duration)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols-1][self._num_rows-1].has_bottom_wall = False
        self._draw_cell(self._num_cols-1, self._num_rows-1)

    def _break_walls(self, i, j):
        self._cells[i][j].visited = True
        while True:
            to_visit = []
            if i+1 < self._num_cols and not self._cells[i+1][j].visited:
                to_visit.append((i+1, j))
            if i-1 >= 0 and not self._cells[i-1][j].visited:
                to_visit.append((i-1, j))
            if j+1 < self._num_rows and not self._cells[i][j+1].visited:
                to_visit.append((i, j+1))
            if j-1 >= 0 and not self._cells[i][j-1].visited:
                to_visit.append((i, j-1))
            if len(to_visit) == 0:
                self._draw_cell(i, j)
                return
            else:
                next_i, next_j = random.choice(to_visit)
            if next_i > i:
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif next_i < i:
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif next_j > j:
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False
            elif next_j < j:
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            self._break_walls(next_i, next_j)

    def _reset_cells_visited(self):
        for col in range(self._num_cols):
            for row in range(self._num_rows):
                self._cells[col][row].visited = False

    def solve(self):
        return self._solve_r(i=0, j=0)

    def _solve_r(self, i, j):
        self._animate()
        self._cells[i][j].visited = True
        if self._cells[self._num_cols-1][self._num_rows-1].visited:
            return True
        if i+1 < self._num_cols and self._cells[i][j].has_right_wall == False and not self._cells[i+1][j].visited:
            self._cells[i][j].draw_move(self._cells[i+1][j])
            if self._solve_r(i+1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i+1][j], undo=True)
        if i-1 >= 0 and self._cells[i][j].has_left_wall == False and not self._cells[i-1][j].visited:
            self._cells[i][j].draw_move(self._cells[i-1][j])
            if self._solve_r(i-1, j):
                return True
            self._cells[i][j].draw_move(self._cells[i-1][j], undo=True)
        if j+1 < self._num_rows and self._cells[i][j].has_bottom_wall == False and not self._cells[i][j+1].visited:
            self._cells[i][j].draw_move(self._cells[i][j+1])
            if self._solve_r(i, j+1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j+1], undo=True)
        if j-1 >= 0 and self._cells[i][j].has_top_wall == False and not self._cells[i][j-1].visited:
            self._cells[i][j].draw_move(self._cells[i][j-1])
            if self._solve_r(i,j-1):
                return True
            self._cells[i][j].draw_move(self._cells[i][j-1], undo=True)
        return False
    