import numpy as np
import pandas as pd

from utils import get_accuracy
from Perceptron import Perceptron as NeuralNetwork

# Read data from a CSV file
data_test = pd.read_csv('./dataset/emnist-letters-test.csv')

data_test = np.array(data_test)
m, n = data_test.shape

data_train = data_test.T
Y_test = data_train[0]
X_test = data_train[1:n]
X_test = X_test / 255.


# Read data from a CSV file
data = pd.read_csv('./dataset/emnist-letters-train.csv')

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
  'hidden_size': 200,
  'output_size': 27,
  'num_samples': m,
  'alpha': 0.1,
  'iterations': 300
}


nn = NeuralNetwork(config)
W1, b1, W2, b2 = nn.train(X_train, Y_train)
dev_predictions = nn.make_predictions(X_test, W1, b1, W2, b2)

accuracy = get_accuracy(dev_predictions, Y_test)
print("Accuracy: ", accuracy)

# save the model
np.savez('model-letters.npz', W1=W1, b1=b1, W2=W2, b2=b2)