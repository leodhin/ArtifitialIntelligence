import numpy as np
import pandas as pd

from utils import get_accuracy
from Perceptron import Perceptron as NeuralNetwork

# Read data from a CSV file
data = pd.read_csv('./train.csv')
head = data.head()

# Convert the data to a NumPy array
data = np.array(data)
m, n = data.shape
np.random.shuffle(data) # shuffle before splitting into dev and training sets

data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n]
X_dev = X_dev / 255.

data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.
_,m_train = X_train.shape


config = {
  'input_size': 784,
  'hidden_size': 128,
  'output_size': 10,
  'num_samples': m,
  'alpha': .5,
  'iterations': 500
}

nn = NeuralNetwork(config)
W1, b1, W2, b2 = nn.train(X_train, Y_train)
dev_predictions = nn.make_predictions(X_dev, W1, b1, W2, b2)

get_accuracy(dev_predictions, Y_dev)

# save the model
np.savez('model-digits.npz', W1=W1, b1=b1, W2=W2, b2=b2)