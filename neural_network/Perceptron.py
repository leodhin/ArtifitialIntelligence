import numpy as np
from utils import get_predictions, get_accuracy, ReLU, softmax, one_hot, ReLU_deriv

# Define the Perceptron class
class Perceptron:
    def __init__(self, config):
        self.n_input_neurons = config['input_size']
        self.n_hidden_neurons = config['hidden_size']  # Number of neurons in the hidden layer
        self.n_output_neurons = config['output_size']
        self.alpha = config['alpha']
        self.iterations = config['iterations']
        self.m = config['num_samples']

        self.W1, self.b1, self.W2, self.b2 = self.init_params()
      
    def init_params(self):
        W1 = np.random.rand(self.n_hidden_neurons, self.n_input_neurons) - 0.5
        b1 = np.random.rand(self.n_hidden_neurons, 1) - 0.5
        W2 = np.random.rand(self.n_output_neurons, self.n_hidden_neurons) - 0.5
        b2 = np.random.rand(self.n_output_neurons, 1) - 0.5
        return W1, b1, W2, b2
      
    def update_params(self, W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
        W1 = W1 - alpha * dW1
        b1 = b1 - alpha * db1    
        W2 = W2 - alpha * dW2  
        b2 = b2 - alpha * db2    
        return W1, b1, W2, b2
  
    def forward_prop(self, W1, b1, W2, b2, X):
        Z1 = W1.dot(X) + b1
        A1 = ReLU(Z1)
        Z2 = W2.dot(A1) + b2
        A2 = softmax(Z2)
        return Z1, A1, Z2, A2
  
    def train(self, X, Y):
        W1, b1, W2, b2 = self.init_params()
        for i in range(self.iterations):
            Z1, A1, Z2, A2 = self.forward_prop(W1, b1, W2, b2, X)
            dW1, db1, dW2, db2 = self.backward_prop(Z1, A1, A2, W2, X, Y, self.m)
            W1, b1, W2, b2 = self.update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, self.alpha)
            if i % 10 == 0:
                print("Iteration: ", i)
                predictions = get_predictions(A2)
                print(get_accuracy(predictions, Y))
        return W1, b1, W2, b2
  
    def backward_prop(self, Z1, A1, A2, W2, X, Y, m):
        one_hot_Y = one_hot(Y)
        dZ2 = A2 - one_hot_Y
        dW2 = 1 / m * dZ2.dot(A1.T)
        db2 = 1 / m * np.sum(dZ2, axis=1, keepdims=True)
        dZ1 = W2.T.dot(dZ2) * ReLU_deriv(Z1)
        dW1 = 1 / m * dZ1.dot(X.T)
        db1 = 1 / m * np.sum(dZ1, axis=1, keepdims=True)
        return dW1, db1, dW2, db2
  
    def make_predictions(self, X, W1, b1, W2, b2):
        _, _, _, A2 = self.forward_prop(W1, b1, W2, b2, X)
        predictions = get_predictions(A2)
        return predictions