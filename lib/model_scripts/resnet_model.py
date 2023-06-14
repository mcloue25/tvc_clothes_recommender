import os
import matplotlib.pyplot as plt
import numpy as np
import argparse

from imutils import paths
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import AveragePooling2D
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications import ResNet50
from sklearn.metrics import classification_report


def augment():
    # initialize the training training data augmentation object
    trainAug = ImageDataGenerator(
        rotation_range=25,
        zoom_range=0.1,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.2,
        horizontal_flip=True,
        fill_mode="nearest")

    # initialize the validation/testing data augmentation object (which
    # we'll be adding mean subtraction to)
    valAug = ImageDataGenerator()
    # define the ImageNet mean subtraction (in RGB order) and set the
    # the mean subtraction value for each of the data augmentation
    # objects
    mean = np.array([123.68, 116.779, 103.939], dtype="float32")
    trainAug.mean = mean
    valAug.mean = mean



def main():
    '''
    Plan for the next while:
    Fashion MNIST & DeepFashion model for bounding box
    Use bounding box to find tagret location (Regions of Interest)
    Classification
    '''

    dataset_path = 'labelled_dataset/'
    batch_size = 32
    img_height = 300
    img_width = 300
    
    train_ds, val_ds, class_names = create_test_train(dataset_path, img_height, img_width, batch_size)

    create_folder('models/')
    model, history, epochs = create_model(train_ds, val_ds, class_names, img_height, img_width, batch_size)
 
    get_model_summary(model)

    create_folder('saved_model/')

    model.save('saved_model/basic_model')

    # How to reload model
    # new_model = tf.keras.models.load_model('models/basic_model')


if __name__ == "__main__":
    main()