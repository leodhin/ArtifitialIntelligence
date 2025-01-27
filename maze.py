import tkinter as tk

maze = [
    ['S', 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 0, 'E'],
]

window = tk.Tk()
window.title("Hello World")

PIXE_SIZE = 100
canvas = tk.Canvas(window, bg="grey", width=len(maze) * PIXE_SIZE, height=len(maze) * PIXE_SIZE)



for i, row in enumerate(maze):
    for j, cell in enumerate(row):
        # Calculate pixel positions
        x1 = j * PIXE_SIZE
        y1 = i * PIXE_SIZE
        x2 = x1 + PIXE_SIZE
        y2 = y1 + PIXE_SIZE
        
        # Draw the rectangles based on cell type
        if cell == 0:
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", width=1)
        elif cell == 1:
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="white", width=1)
        elif cell == 'S':
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="red", width=1)
        elif cell == 'E':
            print(cell)
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green", width=1)
        else:
            canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black", width=1)

def handle_button_press(event):
    window.destroy()

canvas.pack()

# Start the event loop.
window.mainloop()