import tkinter as tk
import json as json

import Cell as Cell
from constants import PIXE_SIZE

class GUI:
    def __init__(self, maze):
        self.maze = maze
        self.window = tk.Tk()
        self.window.title("Hello World")

        self.canvas = tk.Canvas(self.window, bg="grey", width=len(maze) * PIXE_SIZE, height=len(maze) * PIXE_SIZE)
        self.canvas.pack()
        print("GUI initialized")
        
    def fill_tile(self, cell: Cell, color: str):
        x1 = cell.pos.x * PIXE_SIZE
        y1 = cell.pos.y * PIXE_SIZE
        x2 = x1 + PIXE_SIZE
        y2 = y1 + PIXE_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, width=1)
        self.window.update()
    
    def color_border(self, cell: Cell, color: str):
        x1 = cell.pos.x * PIXE_SIZE
        y1 = cell.pos.y * PIXE_SIZE
        x2 = x1 + PIXE_SIZE
        y2 = y1 + PIXE_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, outline=color, width=3)
        self.window.update()