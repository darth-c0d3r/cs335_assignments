import numpy as np

class FullyConnectedLayer:
	def __init__(self, in_nodes, out_nodes):
		# Method to initialize a Fully Connected Layer
		# Parameters
		# in_nodes - number of input nodes of this layer
		# out_nodes - number of output nodes of this layer
		self.in_nodes = in_nodes
		self.out_nodes = out_nodes
		# Stores the outgoing summation of weights * features 
		self.data = None

		# Initializes the Weights and Biases using a Normal Distribution with Mean 0 and Standard Deviation 0.1
		self.weights = np.random.normal(0,0.1,(in_nodes, out_nodes))	
		self.biases = np.random.normal(0,0.1, (1, out_nodes))
		###############################################
		# NOTE: You must NOT change the above code but you can add extra variables if necessary 

	def forwardpass(self, X):
		# print('Forward FC ',self.weights.shape)
		# Input
		# activations : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer

		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_nodes]
		# OUTPUT activation matrix		:[n X self.out_nodes]

		###############################################
		# TASK 1 - YOUR CODE HERE
		self.data = np.matmul(X,self.weights) + np.repeat(self.biases, n, axis=0)
		return sigmoid(self.data)

		# raise NotImplementedError
		###############################################
		
	def backwardpass(self, lr, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		# Update self.weights and self.biases for this layer by backpropagation
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		# assuming delta is nxk and activation_prev is nxj
		wgrad_matrix = np.zeros(self.weights.shape)
		bgrad_matrix = np.zeros(self.biases.shape)
		new_delta = np.zeros((n,self.in_nodes))
		for r in range(n):
			hadamard = delta[r,:] * derivative_sigmoid(self.data[r,:])
			hadamard = np.reshape(hadamard, (hadamard.shape[0], -1))
		
			wgrad_matrix += np.transpose(np.matmul(hadamard, np.reshape(activation_prev[r,:], (self.in_nodes,-1)).T))
			bgrad_matrix += hadamard.T

			new_delta[r,:] = np.matmul(self.weights, hadamard).T

		self.weights -= lr * wgrad_matrix
		self.biases  -= lr * bgrad_matrix

		return new_delta
		# raise NotImplementedError
		###############################################

class ConvolutionLayer:
	def __init__(self, in_channels, filter_size, numfilters, stride):
		# Method to initialize a Convolution Layer
		# Parameters
		# in_channels - list of 3 elements denoting size of input for convolution layer
		# filter_size - list of 2 elements denoting size of kernel weights for convolution layer
		# numfilters  - number of feature maps (denoting output depth)
		# stride	  - stride to used during convolution forward pass
		self.in_depth, self.in_row, self.in_col = in_channels
		self.filter_row, self.filter_col = filter_size
		self.stride = stride

		self.out_depth = numfilters
		self.out_row = int((self.in_row - self.filter_row)/self.stride + 1)
		self.out_col = int((self.in_col - self.filter_col)/self.stride + 1)

		# Stores the outgoing summation of weights * feautres
		self.data = None
		
		# Initializes the Weights and Biases using a Normal Distribution with Mean 0 and Standard Deviation 0.1
		self.weights = np.random.normal(0,0.1, (self.out_depth, self.in_depth, self.filter_row, self.filter_col))	
		self.biases = np.random.normal(0,0.1, self.out_depth)
		

	def forwardpass(self, X):
		# print('Forward CN ',self.weights.shape)
		# Input
		# X : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_depth X self.in_row X self.in_col]
		# OUTPUT activation matrix		:[n X self.out_depth X self.out_row X self.out_col]

		###############################################
		# TASK 1 - YOUR CODE HERE
		self.data = np.zeros((n,self.out_depth, self.out_row, self.out_col))
		for i in range(self.out_row):
			for j in range(self.out_col):
				data = X[:,:, i*self.stride : i*self.stride+self.filter_row, j*self.stride : j*self.stride+self.filter_col]

				data = data.reshape(n,-1)
				kern = np.transpose(self.weights.reshape(self.out_depth,-1))
				bias = np.repeat(self.biases.reshape(1,self.biases.shape[0]), n, axis=0)
				
				self.data[:,:,i,j] = (np.matmul(data,kern)+bias).reshape((n, self.out_depth))
		return sigmoid(self.data)
		# raise NotImplementedError
		###############################################

	def backwardpass(self, lr, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		# Update self.weights and self.biases for this layer by backpropagation
		n = activation_prev.shape[0] # batch size

		###############################################
		# TASK 2 - YOUR CODE HERE
		wgrad_matrix = np.zeros(self.weights.shape)
		bgrad_matrix = np.zeros(self.biases.shape)
		new_delta = np.zeros((n,self.in_depth, self.in_row, self.in_col))

		for r in range(n):
			hadamard = delta[r,:,:,:] * derivative_sigmoid(self.data[r,:,:,:])
			for d in range(self.out_depth):
				for i in range(self.out_row):
					for j in range(self.out_col):
						i1 = i*self.stride
						i2 = i1+self.filter_row
						j1 = j*self.stride
						j2 = j1+self.filter_col
						
						wgrad_matrix[d,:,:,:] += hadamard[d,i,j] * activation_prev[r,:,i1:i2,j1:j2]
						bgrad_matrix[d] += hadamard[d,i,j]
						new_delta[r,:,i1:i2,j1:j2] += hadamard[d,i,j] * self.weights[d,:,:,:]

		self.weights -= lr * wgrad_matrix
		self.biases  -= lr * bgrad_matrix

		return new_delta

		# raise NotImplementedError
		###############################################
	
class AvgPoolingLayer:
	def __init__(self, in_channels, filter_size, stride):
		# Method to initialize a Convolution Layer
		# Parameters
		# in_channels - list of 3 elements denoting size of input for max_pooling layer
		# filter_size - list of 2 elements denoting size of kernel weights for convolution layer

		# NOTE: Here we assume filter_size = stride
		# And we will ensure self.filter_size[0] = self.filter_size[1]
		self.in_depth, self.in_row, self.in_col = in_channels
		self.filter_row, self.filter_col = filter_size
		self.stride = stride

		self.out_depth = self.in_depth
		self.out_row = int((self.in_row - self.filter_row)/self.stride + 1)
		self.out_col = int((self.in_col - self.filter_col)/self.stride + 1)

	def forwardpass(self, X):
		# print('Forward MP ')
		# Input
		# X : Activations from previous layer/input
		# Output
		# activations : Activations after one forward pass through this layer
		
		n = X.shape[0]  # batch size
		# INPUT activation matrix  		:[n X self.in_depth X self.in_row X self.in_col]
		# OUTPUT activation matrix		:[n X self.out_depth X self.out_row X self.out_col]

		###############################################
		# TASK 1 - YOUR CODE HERE
		out = np.zeros((n,self.out_depth, self.out_row, self.out_col))
		for i in range(self.out_row):
			for j in range(self.out_col):
				data = X[:,:, i*self.stride : i*self.stride+self.filter_row, j*self.stride : j*self.stride+self.filter_col]
				data = data.reshape(n,self.out_depth,-1)
				out[:,:,i,j] = np.mean(data, axis=2)
		return out
		# raise NotImplementedError
		###############################################


	def backwardpass(self, alpha, activation_prev, delta):
		# Input
		# lr : learning rate of the neural network
		# activation_prev : Activations from previous layer
		# activations_curr : Activations of current layer
		# delta : del_Error/ del_activation_curr
		# Output
		# new_delta : del_Error/ del_activation_prev
		
		n = activation_prev.shape[0] # batch size
		

		###############################################
		# TASK 2 - YOUR CODE HERE
		k = self.stride
		# in = n * d * a * b [delta]
		# out = n * d * ka * kb
		out = np.zeros(activation_prev.shape)
		out[:,:,:delta.shape[2]*k, :delta.shape[3]*k] = np.repeat(np.repeat(delta,k,axis=2),k,axis=3)/(k*k)
		return out
		# raise NotImplementedError
		###############################################


# Helper layer to insert between convolution and fully connected layers
class FlattenLayer:
    def __init__(self):
        pass
    
    def forwardpass(self, X):
        self.in_batch, self.r, self.c, self.k = X.shape
        return X.reshape(self.in_batch, self.r * self.c * self.k)

    def backwardpass(self, lr, activation_prev, delta):
        return delta.reshape(self.in_batch, self.r, self.c, self.k)


# Helper Function for the activation and its derivative
def sigmoid(x):
	return 1 / (1 + np.exp(-x))

def derivative_sigmoid(x):
	return sigmoid(x) * (1 - sigmoid(x))
