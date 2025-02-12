import numpy as np

# Define the Neuron class
class Neuron:
  value = None
  def __init__(self, value):
    self.value = value

# Define the Perceptron class
class Perceptron:
  n_input_neurons = None
  n_output_neurons = None
  
  def __init__(self, n_input_neurons, n_output_neurons):
      self.n_input_neurons = n_input_neurons
      self.n_output_neurons = n_output_neurons
      self.W1, self.b1, self.W2, self.b2 = self.init_params()
      
  def init_params(self):
      W1 = np.random.rand(self.n_output_neurons, self.n_input_neurons) - 0.5 # 10 neurons in the first hidden layer, 784 input features - Matrix 10rowsx784columns
      b1 = np.random.rand(self.n_output_neurons, 1) - 0.5  # Bias for the 10 neurons in the first hidden layer
      W2 = np.random.rand(self.n_output_neurons, self.n_output_neurons) - 0.5 # 10 neurons in the output layer, 10 neurons in the hidden layer Matrix 10rowsx10columns
      b2 = np.random.rand(self.n_output_neurons, 1) - 0.5  # Bias for the 10 neurons in the output layer
      return W1, b1, W2, b2
      
  def update_params(self, W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1    
    W2 = W2 - alpha * dW2  
    b2 = b2 - alpha * db2    
    return W1, b1, W2, b2