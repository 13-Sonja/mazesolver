from tkinter import Tk, BOTH, Canvas


class Window():
    def __init__(self, height, width):
        self.root = Tk()
        self.root.title("Maze Solver")
        self.canvas = Canvas(self.root, height=height, width=width, background="light gray")
        self.canvas.pack(fill=BOTH, expand=1)
        self.running = False
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()
    
    def wait_for_close(self):
        self.running = True
        while self.running:
            self.redraw()
    
    def close(self):
        self.running = False

    def draw_line(self, line, fill_colour="black"):
        line.draw(self.canvas, fill_colour)    


class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line():
    def __init__(self, point_a, point_b):
        self.point_a = point_a
        self.point_b = point_b

    def draw(self, canvas, fill_colour):
        canvas.create_line(self.point_a.x, self.point_a.y, self.point_b.x, self.point_b.y, fill=fill_colour, width=2)
        canvas.pack(fill=BOTH, expand=1)
