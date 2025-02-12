import numpy as np
import pandas as pd

from utils import forward_prop, backward_prop

# Read data from a CSV file
data = pd.read_csv('./emnist-letters-train.csv')
head = data.head()

# Convert the data to a NumPy array
data = np.array(data)
m, n = data.shape

data_train = data.T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.
_,m_train = X_train.shape

# weight and biases
def init_params():
    W1 = np.random.rand(27, 784) - 0.5  # 26 neurons in the first hidden layer, 784 input features (28x28 image flattened)
    b1 = np.random.rand(27, 1) - 0.5   # Bias for the 26 neurons in the first hidden layer
    W2 = np.random.rand(27, 27) - 0.5  # 26 neurons in the output layer, 26 neurons in the hidden layer
    b2 = np.random.rand(27, 1) - 0.5   # Bias for the 26 neurons in the output layer
    return W1, b1, W2, b2

def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1    
    W2 = W2 - alpha * dW2  
    b2 = b2 - alpha * db2    
    return W1, b1, W2, b2

def get_predictions(A2):
    return np.argmax(A2, 0)

def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions

def get_accuracy(predictions, Y):
    print(predictions, Y)
    return np.sum(predictions == Y) / Y.size

def gradient_descent(X, Y, alpha, iterations):
    W1, b1, W2, b2 = init_params()
    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, A2, W2, X, Y, m)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
        if i % 10 == 0:
            print("Iteration: ", i)
            predictions = get_predictions(A2)
            print(get_accuracy(predictions, Y))
    return W1, b1, W2, b2

W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 1, 500)

# save the model
np.savez('model-letters.npz', W1=W1, b1=b1, W2=W2, b2=b2)