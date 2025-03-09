from utils import forward_prop, backward_prop

import numpy as np
from tkinter import *
from tkinter import filedialog
import PIL
from PIL import Image, ImageDraw

# Global variables for models
model_horses_humans = np.load('model-horse-human.npz')

W1, b1, W2, b2 = model_horses_humans['W1'], model_horses_humans['b1'], model_horses_humans['W2'], model_horses_humans['b2']

def ReLU(Z):
    return np.maximum(0, Z)

def softmax(Z):
    A = np.exp(Z) / np.sum(np.exp(Z), axis=0, keepdims=True)
    return A

def get_predictions(A2):
    return np.argmax(A2, 0)

def preprocess_image(image):
    image = image.convert('L')  # Convert to grayscale
    image = image.resize((28, 28))  # Resize to 28x28
    image = np.array(image).flatten() / 255.0  # Flatten to 1D array and normalize
    image = image.reshape(784, 1)  # Reshape to (784, 1)
    return image

def predict(image, W1, b1, W2, b2):
    X = preprocess_image(image)
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X, 2)
    predictions = get_predictions(A2)
    return predictions

def clear():
    cv.delete("all")
    draw.rectangle([0, 0, 280, 280], fill="black")

def import_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        image = Image.open(file_path)
        predictions = predict(image, W1, b1, W2, b2)
        output = "Horse" if predictions[0] == 1 else "Human"
        prediction.config(text="Prediction: " + output)
        print(output)

def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1, y1, x2, y2, fill="white", width=15)
    draw.line([x1, y1, x2, y2], fill=255, width=15)

root = Tk()
cv = Canvas(root, width=280, height=280, bg='white')
cv.pack()

image = PIL.Image.new("L", (280, 280), 0)
draw = ImageDraw.Draw(image)
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

import_button = Button(text="Import Image", command=import_image)
import_button.pack()

clear_button = Button(text="Clear", command=clear)
clear_button.pack()

prediction = Label(text="Prediction: ")
prediction.pack()

root.mainloop()