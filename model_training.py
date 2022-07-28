import os
import cv2
import tensorflow
from tensorflow.keras.datasets import fashion_mnist


def load_mnist_data():
    ((trainX, trainY), (testX, testY)) = fashion_mnist.load_data()

def main():
    '''
    Plan for the next while:
    Fashion MNIST & DeepFashion model for bounding box
    Use bounding box to find tagret location (Regions of Interest)
    Classification
    '''
    load_data()


if __name__ == "__main__":
    main()