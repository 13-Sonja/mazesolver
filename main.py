from graphics import Window
from maze import Maze

HEIGHT, WIDTH = 950, 950


def main():
    win = Window(HEIGHT, WIDTH)
    maze = Maze(15, 15, 20, 20, 40, 40, win, 13)
    maze.solve()
    win.wait_for_close()

if __name__ == "__main__":
    main()