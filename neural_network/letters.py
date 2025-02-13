import numpy as np
import pandas as pd

from utils import get_accuracy
from Perceptron import Perceptron as NeuralNetwork

# Read data from a CSV file
data = pd.read_csv('./emnist-letters-train.csv')
head = data.head()

# Convert the data to a NumPy array
data = np.array(data)
m, n = data.shape

data_train = data.T
# Gets the first row of the data which is the label
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.


config = {
  'input_size': 784,
  'hidden_size': 128,
  'output_size': 27,
  'num_samples': m,
  'alpha': .5,
  'iterations': 500
}


nn = NeuralNetwork(config)
W1, b1, W2, b2 = nn.train(X_train, Y_train)
dev_predictions = nn.make_predictions(X_train, W1, b1, W2, b2)

get_accuracy(dev_predictions, Y_train)

# save the model
np.savez('model-letters.npz', W1=W1, b1=b1, W2=W2, b2=b2)