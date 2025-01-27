import tkinter as tk
import json as json

from Cell import Cell

with open('maze1.json') as f:
    maze = json.load(f)

actual = (0, 0)
start = None
end = None


mapped_maze = []

window = tk.Tk()
window.title("Hello World")

PIXE_SIZE = 100
canvas = tk.Canvas(window, bg="grey", width=len(maze) * PIXE_SIZE, height=len(maze) * PIXE_SIZE)


        
def draw_maze():
    global start
    global end
    for i, row in enumerate(maze):
        for j, tile in enumerate(row):
            # Calculate pixel positions
            x1 = j * PIXE_SIZE
            y1 = i * PIXE_SIZE
            x2 = x1 + PIXE_SIZE
            y2 = y1 + PIXE_SIZE
            
            newCell = Cell((i, j), None)
            # Draw the rectangles based on cell type
            if tile == 0:
                fill_color = "black"
            elif tile == 1:
                newCell.isWalkable = True
                fill_color = "white"
            elif tile == 'S':
                newCell.isStart = True
                start = (i, j)
                fill_color = "red"
            elif tile == 'E':
                newCell.isEnd = True
                fill_color = "green"
                end = (i, j)
            
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=fill_color, width=1)
            canvas.create_text(x1 + 90, y1 + 90, text= newCell.calculateHeuristic(), fill="black", anchor="se")
            mapped_maze.append(newCell)
            

def get_neighbors(cell):
    i, j = cell
    neighbors = []
    # Check if the cell is the left wall
    if i > 0:
        neighbors.append((i - 1, j))
    # Check if the cell is the right wall
    if i < len(maze) - 1:
        neighbors.append((i + 1, j))
    # Check if the cell is the top wall
    if j > 0:
        neighbors.append((i, j - 1))
    # Check if the cell is the bottom wall
    if j < len(maze[i]) - 1:
        neighbors.append((i, j + 1))
        
        print(neighbors)
    return neighbors

def a_star():    
    open_list = []
    closed_list = []
    
    start_cell = mapped_maze[start[0] * len(maze) + start[1]]
    start_cell.calculateValues()
    open_list.append(start_cell)
    
    while len(open_list) > 0:
        current_cell = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_cell.f:
                current_cell = item
                current_index = index
        
        open_list.pop(current_index)
        closed_list.append(current_cell)
        
        if current_cell.pos == end:
            path = []
            current = current_cell
            while current is not None:
                path.append(current.pos)
                current = current.parent
            print(path)
            break
        
        children = []
        for new_position in get_neighbors(current_cell.pos):
            new_cell = mapped_maze[new_position[0] * len(maze) + new_position[1]]
            
            if not new_cell.isWalkable or new_cell in closed_list:
                continue
            
            new_cell.calculateValues()
            children.append(new_cell)
            
        for child in children:
            for closed_child in closed_list:
                if child == closed_child:
                    continue
            
            child.calculateValues()
            if child not in open_list:
                open_list.append(child)
        
        print("Open list: ", open_list)
        print("Closed list: ", closed_list)
        print("Visited list: ", visited)
        print("Current cell: ", current_cell.pos)
        print("Current cell f: ", current_cell.f)
        print("Current cell g: ", current_cell.g)
        print("Current cell h: ", current_cell.h)
        print("Current cell parent: ", current_cell.parent)
        print("\n")
        visited.append(current_cell)
        draw_path(visited)
        draw_path(closed_list)

if __name__ == "__main__":
    canvas.pack()
    draw_maze()
    #a_star()
    
    # Start the event loop.
    window.mainloop()
