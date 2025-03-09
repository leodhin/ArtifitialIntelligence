import numpy as np
import pandas as pd
from PIL import Image

from utils import get_accuracy
from Perceptron import Perceptron as NeuralNetwork

horse_dataset = []
human_dataset = []

# Load horse data
for i in range(1, 50):
    for j in range(0, 9):
        try:
            horse = Image.open(f"dataset/humans-horses/train/horses/horse{i:02d}-{j}.png")
            horse = horse.resize((28, 28)).convert('L')
            horse = np.array(horse).flatten() / 255.0
            horse_dataset.append(horse)
        except FileNotFoundError:
            print(f"File not found: dataset/humans-horses/train/horses/horse{i:02d}-{j}.png")

# Load human data
for i in range(1, 18):
    for j in range(0, 30):
        try:
            human = Image.open(f"dataset/humans-horses/train/humans/human{i:02d}-{j:02d}.png")
            human = human.resize((28, 28)).convert('L')
            human = np.array(human).flatten() / 255.0
            human_dataset.append(human)
        except FileNotFoundError:
            print(f"File not found: dataset/humans-horses/train/humans/human{i:02d}-{j:02d}.png")

# Combine datasets and create labels
data_train = np.array(horse_dataset + human_dataset)
Y_train = np.array([1] * len(horse_dataset) + [0] * len(human_dataset))
X_train = data_train.T


config = {
    'input_size': 784,
    'hidden_size': 200,
    'output_size': 2,
    'num_samples': len(horse_dataset) + len(human_dataset),
    'alpha': 0.1,
    'iterations': 500
}

nn = NeuralNetwork(config)
W1, b1, W2, b2 = nn.train(X_train, Y_train)


# Load test data
horse_dataset = []
human_dataset = []

# Load horse data
for i in range(1, 6):
    for j in range(0, 9):
        try:
            horse = Image.open(f"dataset/humans-horses/test/horses/horse{i:03d}-{j:03d}.png")
            horse = horse.resize((28, 28)).convert('L')
            horse = np.array(horse).flatten() / 255.0
            horse_dataset.append(horse)
        except FileNotFoundError:
            print(f"File not found: dataset/humans-horses/test/horses/horse{i:03d}-{j:03d}.png")
            
# Load human data
for i in range(1, 5):
    for j in range(0, 23):
        try:
            human = Image.open(f"dataset/humans-horses/test/humans/valhuman{i:02d}-{j:02d}.png")
            human = human.resize((28, 28)).convert('L')
            human = np.array(human).flatten() / 255.0
            human_dataset.append(human)
        except FileNotFoundError:
            print(f"File not found: dataset/humans-horses/test/humans/valhuman{i:02d}-{j:02d}.png")
            
# Combine datasets and create labels
data_test = np.array(horse_dataset + human_dataset)
data_test = data_test.T

Y_test = np.array([1] * len(horse_dataset) + [0] * len(human_dataset))

dev_predictions = nn.make_predictions(data_test, W1, b1, W2, b2)


# Get the accuracy of the model
accuracy = get_accuracy(dev_predictions, Y_test)
print("Accuracy:", accuracy)

# Save the model
np.savez('model-horse-human.npz', W1=W1, b1=b1, W2=W2, b2=b2)