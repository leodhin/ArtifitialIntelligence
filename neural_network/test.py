from utils import forward_prop, backward_prop

import numpy as np
from tkinter import *
import PIL
from PIL import Image, ImageDraw
# import model.npz file
model = np.load('model-digits.npz')

W1 = model['W1']
b1 = model['b1']
W2 = model['W2']
b2 = model['b2']

#function to decode number into letter (1-26)
def decode(number):
    return chr(number + 97)

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
    image = np.array(image).flatten() / 255.0 # Flatten to 1D array
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
    cv.create_oval(x1, y1, x2, y2, fill="white", width=15)
    draw.line([x1, y1, x2, y2], fill=255, width=15)

def update_model():
    global W1, b1, W2, b2

    # Obtener la entrada del usuario y limpiar espacios
    real_value = entry.get().strip()

    # Validar que la entrada no esté vacía y sea un número
    if not real_value.isdigit():
        prediction.config(text="❌ Error: Introduce un número entre 0 y 9")
        return  # Salir sin actualizar el modelo

    # Convertir a entero
    real_value = int(real_value)

    # Asegurar que está dentro del rango 0-9
    if real_value < 0 or real_value > 9:
        prediction.config(text="❌ Error: Solo se permiten números del 0 al 9")
        return

    X = preprocess_image(image)

    # Obtener la propagación hacia adelante
    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
    
    # Crear la etiqueta correcta en formato one-hot (para números 0-9)
    one_hot_Y = np.zeros((10, 1))  # 10 clases (0-9)
    one_hot_Y[real_value] = 1  
    
    dZ2 = A2 - one_hot_Y
    dW2 = dZ2.dot(A1.T)
    db2 = np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * (Z1 > 0)  
    dW1 = dZ1.dot(X.T)
    db1 = np.sum(dZ1)

    # Aprendizaje en caliente con un pequeño `alpha`
    alpha = 0.1
    W1 -= alpha * dW1
    b1 -= alpha * db1
    W2 -= alpha * dW2
    b2 -= alpha * db2

    # Guardar el modelo actualizado SOLO para números
    np.savez('model-digits.npz', W1=W1, b1=b1, W2=W2, b2=b2)

    prediction.config(text=f"✅ Modelo actualizado con: {real_value}")



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

button_update = Button(root, text="Actualizar Modelo", command=update_model)
button_update.pack()

entry = Entry(root)
entry.pack()




root.mainloop()
