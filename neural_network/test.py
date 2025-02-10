from utils import forward_prop, backward_prop

import numpy as np
from tkinter import *
import PIL
from PIL import Image, ImageDraw
# import model.npz file
model = np.load('model.npz')

W1 = model['W1']
b1 = model['b1']
W2 = model['W2']
b2 = model['b2']

#function to decode number into letter (1-26)
def decode(number):
    return chr(number + 96)

def ReLU(Z):
    return np.maximum(0, Z)

def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A

def get_predictions(A2):
    return np.argmax(A2, 0)

def preprocess_image(image):
    image = image.convert('L')  # Convert to grayscale
    image = image.resize((28, 28))  # Resize to 28x28
    image = np.array(image).flatten()  # Flatten to 1D array
    image = image.reshape(784, 1)  # Reshape to (784, 1)
    
    return image

def predict(image, W1, b1, W2, b2):
    X = preprocess_image(image)
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

def clear():
    cv.delete("all")
    draw.rectangle([0, 0, 280, 280], fill="black")
    
def save():
    filename = "image.png"
    image.resize((28, 28)).save(filename)
    image1 = Image.open(filename)
    predictions = predict(image1, W1, b1, W2, b2)
    prediction.config(text="Prediction: " + str(predictions[0]))
    print(decode(predictions[0]))
    
def paint(event):
    x1, y1 = (event.x - 1), (event.y - 1)
    x2, y2 = (event.x + 1), (event.y + 1)
    cv.create_oval(x1, y1, x2, y2, fill="white", width=5)
    draw.line([x1, y1, x2, y2], fill=255, width=5)
    
root = Tk()
cv = Canvas(root, width=280, height=280, bg='white')
cv.pack()

image = PIL.Image.new("L", (280, 280), 0)
draw = ImageDraw.Draw(image)
cv.pack(expand=YES, fill=BOTH)
cv.bind("<B1-Motion>", paint)

button=Button(text="save",command=save)
button.pack()

clear_button=Button(text="clear",command=clear)
clear_button.pack()

prediction=Label(text="Prediction: ")
prediction.pack()

root.mainloop()
