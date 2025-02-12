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
print(Y_train)
X_train = data_train[1:n]
X_train = X_train / 255.
_,m_train = X_train.shape


nn = NeuralNetwork(784, 27, m)
W1, b1, W2, b2 = nn.train(X_train, Y_train, 1, 500)
dev_predictions = nn.make_predictions(X_train, W1, b1, W2, b2)

get_accuracy(dev_predictions, Y_train)

# save the model
np.savez('model-letters.npz', W1=W1, b1=b1, W2=W2, b2=b2)