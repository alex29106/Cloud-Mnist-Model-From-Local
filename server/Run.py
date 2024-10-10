import numpy as np
import pickle

def feedforward(a,biases,weights):
    for b, w in zip(biases, weights):
        a = sigmoid(np.dot(w,a)+ b)
    return a

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def main(array):
    with open('../resourses/pretrained1.pickle', 'rb') as f:
        biases, weights = pickle.load(f)
        res = np.argmax(feedforward(array,biases, weights))
        return res
