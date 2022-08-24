import os
import cv2
import json
import shutil
import os.path

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

from utils import *

''' Links:
    TF IMAGE CLASSIFICATION: https://www.tensorflow.org/tutorials/images/classification
    TF SAVE & LOAD MODELS:   https://www.tensorflow.org/tutorials/keras/save_and_load
'''


def create_test_train(dataset_path, img_height, img_width, batch_size):
    ''' Used for splitting dataset into test & validation
    '''
    train_ds = tf.keras.utils.image_dataset_from_directory(dataset_path, validation_split=0.2, subset="training", seed=123, image_size=(img_height, img_width), batch_size=batch_size)
    val_ds = tf.keras.utils.image_dataset_from_directory(dataset_path, validation_split=0.2, subset="validation", seed=123, image_size=(img_height, img_width), batch_size=batch_size)  
    class_names = train_ds.class_names

    return train_ds, val_ds, class_names


def get_model_summary(model):
    model.summary()


def create_model(train_ds, val_ds, class_names, img_height, img_width, batch_size):

    # Add buffered prefetching to prevent disk I/O bottlenecking
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Standardize RGB values
    normalization_layer = layers.Rescaling(1./255)
    normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
    image_batch, labels_batch = next(iter(normalized_ds))

    # Data Augmentation
    data_augmentation = tf.keras.Sequential([
            layers.RandomFlip("horizontal_and_vertical"),
            layers.RandomRotation(0.2),])

    
    # Define model
    num_classes = len(class_names)
    model = Sequential([
          layers.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
          data_augmentation,
          layers.Conv2D(16, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Conv2D(32, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Conv2D(64, 3, padding='same', activation='relu'),
          layers.MaxPooling2D(),
          layers.Flatten(),
          layers.Dense(128, activation='relu'),
          layers.Dense(num_classes)
    ])

    # Compile model & train
    model.compile(optimizer='adam',
            loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
            metrics=['accuracy'])

    epochs= 10
    history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs)

    return model, history, epochs


def plot_model_results(history, epochs):
    ''' Used for plotting precision & loss
    '''
    accuracy = history.history['accuracy']
    loss = history.history['loss']
    val_acc = history.history['val_accuracy']
    val_loss = history.history['val_loss']

    epochs_range = range(epochs)

    plt.figure(figsize=(8, 8))
    plt.subplot(1, 2, 1)
    plt.plot(epochs_range, accuracy, label='Training Accuracy')
    plt.plot(epochs_range, val_acc, label='Validation Accuracy')
    plt.legend(loc='lower right')
    plt.title('Training and Validation Accuracy')

    plt.subplot(1, 2, 2)
    plt.plot(epochs_range, loss, label='Training Loss')
    plt.plot(epochs_range, val_loss, label='Validation Loss')
    plt.legend(loc='upper right')
    plt.title('Training and Validation Loss')
    plt.show()



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