import json as json
from Cell import Cell, Coordinates
from gui import GUI

from constants import PIXE_SIZE, WEIGHT_DISTANCE

with open('maze1.json') as f:
    maze = json.load(f)

current = None
start = None
end = None


mapped_maze = [[None for _ in range(len(maze))] for _ in range(len(maze))]

gui = GUI(mapped_maze)

def render_maze():
    global start
    global end
    for i, row in enumerate(maze):
        for j, tile in enumerate(row):
            # Calculate pixel positions
            x1 = i * PIXE_SIZE
            y1 = j * PIXE_SIZE
            coordinates = Coordinates(j, i)
            
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
            mapped_maze[j][i] = newCell
    draw_heuristics()
      
# draw the heuristics
def draw_heuristics():
  for i in range(len(maze)):
      for j in range(len(maze)):
          cell = mapped_maze[i][j]
          gui.canvas.create_text(cell.pos.x * PIXE_SIZE + 90, cell.pos.y * PIXE_SIZE +90, fill="blue", text=(f'h = {cell.calculateHeuristic(end.pos)}'), anchor="se")

          
            

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

def a_star():    
    open_list = []
    closed_list = []
    
    open_list.append(start)
    while(len(open_list) > 0):
        # set interval to 1s
        gui.window.after(200)
        current = open_list[0]
                  

        current_cell = 0
        
        # Order the open list by f value
        for index, cell in enumerate(open_list):
            if cell.f < current.f:
                current = cell
                current_cell = index
                
        open_list.pop(current_cell)
        closed_list.append(current)
        
        # Check if we have reached the end
        if current.isEnd == True:
          gui.fill_tile(current, "purple")
          gui.color_border(current, "red")
          
          while current.parent != None:
            gui.color_border(current.parent, "yellow")
            current = current.parent
          break
        
        children = []
        # Get the neighbors of the current cell
        
        # Iterate over the neighbors and populate the open list
        for neighbour in get_neighbors(current):
            new_cell = mapped_maze[neighbour[0]][neighbour[1]]
            children.append(new_cell)
            if len(closed_list) > 0:
              new_cell.parent = current
              new_cell.calculateValues(end.pos)
            
        for child in children:
            if child in closed_list:
                continue
            
            if child in open_list:
                continue
            
            open_list.append(child)
            gui.canvas.create_text(child.pos.x * PIXE_SIZE + 10, child.pos.y * PIXE_SIZE + 90, fill="blue", text=(f'g = {child.g}'), anchor="sw")
            gui.canvas.create_text(child.pos.x * PIXE_SIZE + 90, child.pos.y * PIXE_SIZE + 10, fill="blue",  text=(f'f = {child.f}'), anchor="ne")
        
        # Color red the border cell
        gui.color_border(current, "red")

    return current

if __name__ == "__main__":
    render_maze()
    result = a_star()
  
    # tick of 1s per loop
    gui.window.mainloop()
