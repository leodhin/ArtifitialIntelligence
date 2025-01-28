import json as json

from Cell import Cell, Coordinates
from gui import GUI

with open('maze1.json') as f:
    maze = json.load(f)

current = None
start = None
end = None


mapped_maze = [[None for _ in range(len(maze))] for _ in range(len(maze))]

gui = GUI(maze)

PIXE_SIZE = 100
        
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
            coordinates = Coordinates(i, j)
            
            newCell = Cell(coordinates, None)
            # Draw the rectangles based on cell type
            if tile == 0:
                fill_color = "black"
                newCell.isWalkable = False
            elif tile == 1:
                newCell.isWalkable = True
                fill_color = "white"
            elif tile == 'S':
                newCell.isStart = True
                start = Cell(coordinates, None)
                fill_color = "red"
            elif tile == 'E':
                newCell.isEnd = True
                fill_color = "green"
                end = Cell(coordinates, None)
            
            gui.fill_tile(newCell, fill_color)
            gui.canvas.create_text(x1 + 90, y1 + 90, text=(f'h = {newCell.calculateHeuristic()}'), fill="black", anchor="se")
            mapped_maze[i][j] = newCell
            
            

def get_neighbors(cell: Cell):
    i, j = cell.pos.x, cell.pos.y
    neighbors = []
    # Check if the cell is the left wall and is isWalkable
    if i > 0 and mapped_maze[i - 1][j].isWalkable:
        neighbors.append((i - 1, j))
    # Check if the cell is the right wall
    if i < len(maze) - 1 and mapped_maze[i + 1][j].isWalkable:
        neighbors.append((i + 1, j))
    # Check if the cell is the top wall
    if j > 0 and mapped_maze[i][j - 1].isWalkable:
        neighbors.append((i, j - 1))
    # Check if the cell is the bottom wall
    if j < len(maze) - 1 and mapped_maze[i][j + 1].isWalkable:
        neighbors.append((i, j + 1))
        
    return neighbors
    

def color_cell(cell: Cell, color: str):
    x1 = cell.pos.y * PIXE_SIZE
    y1 = cell.pos.x * PIXE_SIZE
    x2 = x1 + PIXE_SIZE
    y2 = y1 + PIXE_SIZE
    gui.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, width=1)
    
def a_star():    
    open_list = []
    closed_list = []
    
    open_list.append(start)
  
    while(len(open_list) > 0):
        current = open_list[0]
        
        # Color yellow the current cell
        gui.fill_tile(current, "yellow")
        
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current.f:
                current = item
                current_index = index
        open_list.pop(current_index)
        closed_list.append(current)
        
        if current == end:
            path = []
            current = current
            while current is not None:
                path.append(current.pos)
                current = current.parent
            break
        
        children = []
        for new_position in get_neighbors(current):
            coordinates = Coordinates(new_position[0], new_position[1])
            new_cell = Cell(coordinates, current)
            children.append(new_cell)
        
        for child in children:
            if child in closed_list:
                continue
            
            child.calculateValues()
            
            if child in open_list:
                continue
            
            open_list.append(child)
            
        for child in children:
            gui.canvas.create_text(child.pos.x * PIXE_SIZE + 10, child.pos.y * PIXE_SIZE + 90, text=(f'g = {child.g}'), anchor="sw")
            gui.canvas.create_text(child.pos.x * PIXE_SIZE + 90, child.pos.y * PIXE_SIZE + 10, text=(f'f = {child.f}'), anchor="ne")
    
if __name__ == "__main__":
    draw_maze()
    a_star()
    gui.window.mainloop()
    #get_neighbors(start)
