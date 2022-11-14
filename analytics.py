import os
import cv2
import json
import shutil
import os.path
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot  as plt

from PIL import Image
from tensorflow.keras.utils import load_img
from tensorflow.keras.utils import img_to_array
from keras.models import load_model

from utils import * 

clothes_types = {'coat': ["coat"]}
    

# def get_dataset_pc_classified(json_path, dataset_path):
#     ''' Checks whats precentage of the dataset has been classified
#     '''
#     json_data = import_json(json_path)

#     ids = list(json_data.keys())
#     class_results = list(json_data.values())
#     dataset_size = len(ids)

#     # Calculate % of dataset thats been completed 
#     print("Current length =", dataset_size - 1)
#     print("% Done:", 100 * (dataset_size/len(os.listdir(dataset_path))))


def get_metadata_df(path, json_path):
    ''' Checks if a metadatacsv has already been made & if not creates one form results.json s
    '''
    if os.path.exists(path):
        df = pd.read_csv(path)
        df.set_index("id", inplace=True)
    else:
        df = build_img_df(dataset_path, json_path)
    return df


def build_img_df(folder_path, json_path):
    ''' Used to collect metadata on each image in the dataset
    Args:
        folder_path (String) : A String storing the path to the folder containing the image dataset
    '''
    img_data = []

    json_data = import_json(json_path)

    for image_name in os.listdir(folder_path):
        img = cv2.imread(folder_path + image_name)
        # Store image data
        img_meta = {} 
        img_height, img_width, _ = img.shape
        img_meta["id"] = image_name #image_name.split(".")[0]
        img_meta['class'] = json_data[image_name]
        img_meta["img_height"] = img_height
        img_meta["img_width"] = img_width
        img_meta['height_width_dims'] = str(img_height) + "_" + str(img_width)
        img_meta["aspect_ratio"] = round(img_meta["img_width"] / img_meta["img_height"], 2)
        img_data.append(img_meta)

    # Create DataFrame and save to CSV
    img_df = pd.DataFrame.from_dict(img_data)
    img_df.set_index("id", inplace=True)
    create_csv(img_df, "csv/", "img_metadata.csv")
    
    return img_df


def create_height_width_groups(df):
    ''' Groups the img data based on image height & width so that we can begin experimenting with the largest subset of images
    Args:
        df (DataFrame) : A DataFrame containing all metadata for each image in the dataset
    '''
    # Create grouped DF
    df["img_height_width"] = df["img_height"].astype(str) + "_" + df["img_width"].astype(str)
    grouped_df = df.groupby(['img_height_width']).size().reset_index(name='size')
    
    # Get largest subset
    largest_group = grouped_df.loc[grouped_df['size'].idxmax()]
    largest_subset_df = df.loc[df.img_height_width == largest_group['img_height_width']]

    return grouped_df, largest_subset_df



def segmment_dataset_by_img_dims(metadata_df, grouped_df):
    ''' Creates seperate dataset folders based on image height & width
    '''
    size_path = "size_segmented_dataset/"
    create_folder(size_path)

    for height_width in grouped_df['img_height_width']:
        subset_df = metadata_df.loc[metadata_df['height_width_dims'] == height_width]
        path = size_path + height_width + '.csv'
        create_csv(subset_df, size_path, height_width + '.csv')



def calculate_clothes_type(df, dataset_path):
    ''' Used for calculating what % of the dataset is made up of each clothes type
    '''
    # Different type of clothes item types that we'll use for calculating named distribution of dataset
    clothes_types = ['fleece', 'tee', 't-shirt', 'shirt', 'pants', 'trousers', 'bottoms', 'jacket', 'coat', 'hoodie']
    unnamed_df = df.loc[(df.index.str.startswith('_'))]
    named_df = df.loc[~(df.index.isin(unnamed_df.index))]
    pattern = '|'.join(clothes_types)
    named_df['clothes_type'] = named_df.index.str.contains(pattern)

    # Use keras model to come up with clothes_item_names for each undefined image
    assign_item_types(unnamed_df, dataset_path)
    named_pc_df = named_df['clothes_type'].value_counts(normalize=True).mul(100).astype(str)+'%'

    return named_pc_df


def assign_item_types(unnamed_clothes_df, dataset_path):
    ''' Function used for predicting clothes item types 
    '''
    model = load_model('saved_model/clothes_detection_model')
    unnamed_clothes_df.reset_index(inplace=True)

    # print(unnamed_clothes_df)
    create_folder('data/tmp/')
    for index, row in unnamed_clothes_df.iterrows():

        ''' Error is currently here to do with how im resizing and passing the images of unamed clothes types to the model
        '''
        # Need to find downsizing method that will work best on images 
        image_path = dataset_path + row.id
        image = Image.open(image_path)
        resized_img = image.resize((28, 28), resample=3)
        resized_img.save('data/tmp/test.jpg')

        img = tf.keras.utils.load_img('data/tmp/test.jpg')
        img_array = tf.keras.utils.img_to_array(img)
        img_array = tf.expand_dims(img_array, 0) # Create a batch
        predictions = model.predict(img_array)
        score = tf.nn.softmax(predictions[0])
        print()
        print("This image most likely belongs to {} with a {:.2f} percent confidence.".format(class_names[np.argmax(score)], 100 * np.max(score)))

        print(row)
        a-b

        # Need to get size distribution of image dataset and might change the parameters of the model to best suit the data it will be working with
        


    


def get_class_distribution(df):
    ''' Creates Dataframe for examining class distribution
    '''
    class_df = df.groupby(['class']).size().reset_index(name='count')
    class_df['percent'] = ((class_df['count'] / sum(class_df['count'])) * 100)

    return class_df


def visualise_img_metadata(df, grouped_df):
    ''' Used for plotting the varying sizes of images ocntained in the dataset
    '''
    # show_scatter_plot(df)
    # plot_hist(grouped_df)

    return


def show_scatter_plot(df):
    ''' plots scatter plots
    '''
    plt.scatter(df['img_width'], df.index)
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    points = ax.scatter(df.img_width, df.index, color='blue', alpha=0.5, s=df["aspect_ratio"]*100, picker=True)
    ax.set_title("Image Resolution")
    ax.set_xlabel("width", size=14)
    ax.set_ylabel("height", size=14)
    plt.show()


def plot_hist(df):
    ''' plots histogram
    '''
    ax = df.plot.bar(x = "img_height_width", y = "size", alpha=0.5)
    plt.show()


def create_resized_dataset(df, subset_df):
    ''' reduce image size down to 300 x 300 and keep image qulity 
        LINK: https://www.holisticseo.digital/python-seo/image-optimization/
    '''
    create_folder('resized_dataset/')
    df.reset_index(inplace=True)
    subset_df.reset_index(inplace=True)
    height = int(subset_df.at[0, 'img_height'])
    width = int(subset_df.at[0,'img_width'])

    # Split DF on height x width dimensions
    merged_df = df.merge(subset_df.drop_duplicates(), on=['id','id'], how='left', indicator=True)
    images_to_resize_df = merged_df.loc[(merged_df._merge == 'left_only')]

    # Create resized image dataset
    resize_images(images_to_resize_df, height, width)
    move_subset_images(subset_df, 'clothes_dataset/', 'resized_dataset/')


def move_subset_images(df, src_folder, dest_folder):
    ''' Generic function used for moving images
    '''
    for item in df['id']:
        src_path = src_folder + item
        dest_path = dest_folder + item
        shutil.copy(src_path, dest_path)


def resize_images(df, height, width):
    ''' Resizes images & convert back to RGB to be saved as JPEG's
    '''
    for item in df['id']:
        src_path = 'clothes_dataset/' + item
        image = Image.open(src_path)
        resized_image = image.resize((width, height), resample=1)
        dest_path = 'resized_dataset/' + item

        rgb_im = resized_image.convert('RGB')
        rgb_im.save(dest_path)


def split_dataset(df):
    ''' Used for organizing the dataset to be trained 
        Link: https://www.tensorflow.org/tutorials/images/classification
    '''
    # Create final class folders needed for training
    create_folder('labelled_dataset/')
    create_folder('labelled_dataset/drip/')
    create_folder('labelled_dataset/not_drip/')

    # Split DF into individual class DF's
    df.reset_index(inplace=True)
    drip_df = df.loc[(df['class'] == 'drip')]
    not_drip_df = df.loc[df['class'] == 'not_drip']

    # Move each image to its respective class folder
    move_subset_images(drip_df, 'resized_dataset/', 'labelled_dataset/drip/')
    move_subset_images(not_drip_df, 'resized_dataset/', 'labelled_dataset/not_drip/')


def analytics_main():
    ''' Main script for getting deeper insights into how the dataset is comprised 
    '''
    create_folder("csv/")

    # Load image DF if its been made previously
    path = "data/csv/img_metadata.csv"
    json_path = "data/json/results.json"
    dataset_path = "data/datasets/clothes_dataset/"

    # Load the image metadata DataFrame if its been created previously
    df = get_metadata_df(path, json_path)

    # Will be used for getting analytics as to what portion of of our dataset if made up of each clothes type
    named_pc_df = calculate_clothes_type(df, dataset_path)

    # Calculates what percentage of the dataset has been given a classification 
    # get_dataset_pc_classified(json_path, dataset_path)

    # grouped_df, largest_subset_df = create_height_width_groups(df)

    # Once dataset is annotated resize images to begin training
    # create_resized_dataset(df, largest_subset_df)

    # Split dataset based into class folders
    # split_dataset(df)

    # # Create seperate csv's for each height_width subset
    # segmment_dataset_by_img_dims(df, grouped_df)

    # # Examine class distribution within dataset
    # class_df = get_class_distribution(df)

    # print("LENGTH OF SET:", len(os.listdir(test_folder_path)))

    # Plot the different image dimensions as a scatter plot to see level of disparity & bar chart for volume
    # visualise_img_metadata(df, grouped_df)

if __name__ == "__main__":
    analytics_main()