# perceptron.py
# -------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


# Perceptron implementation
import util
import numpy as np
import sys
import random

PRINT = True

###### DON'T CHANGE THE SEEDS ##########
random.seed(42)
np.random.seed(42)

class PerceptronClassifier:
    """
    Perceptron classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    Note that this time around the weights are referred to just a single lable instead of a list.
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "perceptron"
        self.max_iterations = max_iterations

        ##################IMPORTANT######################
        # The self.weights is just one instance of Counter unlike last time
        #################################################
        self.weights = util.Counter()

    def setWeights(self, weights):
        assert type(weights) == type(self.weights)
        self.weights = weights

    def train( self, trainingData, trainingLabels, sample_weights=None):
        """
        The training loop for the perceptron passes through the training data several
        times and updates the weight vector for each label based on classification errors.
        See the assignment description for details.

        Use the provided self.weights data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        (and thus represents a vector of values).
        """

        self.features = trainingData[0].keys() # could be useful later
        # DO NOT ZERO OUT YOUR WEIGHTS BEFORE STARTING TRAINING, OR
        # THE AUTOGRADER WILL LIKELY DEDUCT POINTS.
        if sample_weights is not None:
            trainingData, trainingLabels = self.sample_data(trainingData, trainingLabels, sample_weights)

        for iteration in range(self.max_iterations):
            for i in range(len(trainingData)): 
                # "*** YOUR CODE HERE ***"
                if self.classify([trainingData[i]])[0] != trainingLabels[i]:
                	if trainingLabels[i] == 1:
                		self.weights += trainingData[i]
                	elif trainingLabels[i] == -1:
                		self.weights -= trainingData[i]

                # util.raiseNotDefined()

    def sample_data(self, trainingData, trainingLabels, sample_weights):
        # "*** YOUR CODE HERE ***"
        sampleSize = int(len(trainingData) * 0.5)

        sampleData = util.Counter()
        sampleLabels = util.Counter()

        # cumulative_weights = sample_weights[:]
        # for i in range(1,len(cumulative_weights)):
        #     cumulative_weights[i] += cumulative_weights[i-1]

        # for i in range(sampleSize):
        #     idx = random.uniform(0.0, 1.0)
        #     for j in range(len(trainingData)):
        #         if idx < cumulative_weights[j]:
        #             sampleData[i] = trainingData[j]
        #             sampleLabels[i] = trainingLabels[j]
        #             break

        samplePairs = util.nSample(sample_weights, zip(trainingData, trainingLabels), sampleSize)
        for i in range(len(samplePairs)):
        	sampleData[i], sampleLabels[i] = samplePairs[i]

        return sampleData, sampleLabels

        # util.raiseNotDefined()

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the assignment description for details.

        Note that this time around the labels are just -1 and 1. 

        Recall that a datum is a util.counter.
        """
        guesses = []
        vectors = util.Counter()
        for datum in data:
            guess = int(np.sign(self.weights * datum))
            if guess == 0:
                guess = np.random.choice(self.legalLabels)
            guesses.append(guess)
        return guesses
