import os
import cv2
import json
import shutil
import os.path

import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.models import Sequential

from analytics import * 


def create_folder_structure(path):

    df = get_metadata_df(path)
    print(df)
    # drip = df.loc[(df.)]


# def train(dataset_path):
#     batch_size = 32
#     img_height = 300
#     img_width = 300

#     # Split dataset
#     train_ds = tf.keras.utils.image_dataset_from_directory(dataset_path, validation_split=0.2, subset="training", seed=123, image_size=(img_height, img_width), batch_size=batch_size)
#     val_ds = tf.keras.utils.image_dataset_from_directory(dataset_path, validation_split=0.2, subset="validation", seed=123, image_size=(img_height, img_width), batch_size=batch_size)

    # Need to rename resized dataset with ther 

def main():
    '''
    Plan for the next while:
    Fashion MNIST & DeepFashion model for bounding box
    Use bounding box to find tagret location (Regions of Interest)
    Classification
    '''
    dataset_path = 'resized_dataset/'
    create_folder_structure(dataset_path)
    a-b
    # train(dataset_path)


if __name__ == "__main__":
    main()