import os
import cv2
import json
import shutil
import os.path

import pandas as pd
import matplotlib.pyplot  as plt


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def get_img_data_df(path):
    # Visualize Image Resolutions
    df = pd.read_csv(path, delimiter=',', sep=r', ')
    df.set_index("id", inplace=True)
    return df

def create_csv(df, path, name):
    print("Creating ", name + ".csv")
    file_path = path + name + ".csv"
    df.to_csv(file_path)
    return

def import_json(json_path):
    """Loads data from a JSON file into a readable JSON object.

    Args: 
        json_path (JSON): A JSON file containing key point information.
    
    Returns:
        jump_height (Int): The height the user has jumped in centimeters.
    """
    with open(json_path, "r") as f:
        json_data = json.load(f)

    return json_data


def build_img_df(folder_path):
    """ Used to collect metadata on each image in our dataset
        Given a folder path constructs a DataFrame consisting of the width, height & aspent ratio values for each image in the folder
    Args:
        folder_path (String) : A String storing the path to the folder containing the image dataset
    """
    img_data = []

    for image_name in os.listdir(folder_path):
        img = cv2.imread(folder_path + image_name)
        # Store image data
        img_meta = {} 
        img_height, img_width, _ = img.shape
        img_meta["id"] = image_name #image_name.split(".")[0]
        img_meta["img_height"] = img_height
        img_meta["img_width"] = img_width
        img_meta['height_width_dims'] = str(img_height) + "_" + str(img_width)
        img_meta["aspect_ratio"] = round(img_meta["img_width"] / img_meta["img_height"], 2)
        img_data.append(img_meta)

    # Create DataFrame and save to CSV
    img_df = pd.DataFrame.from_dict(img_data)
    img_df.set_index("id", inplace=True)
    create_csv(img_df, "csv/", "img_metadata")
    
    return img_df

def visualise_img_metadata(df, grouped_df):

    show_scatter_plot(df)
    plot_hist(grouped_df)

    return

def get_grouped_df(df):
    """ Group df by image height & width so that we can begin experimenting with the largest subset of images
    Args:
        df (DataFrame) : A DataFrame containing all metadata for each image in the dataset
    """
    # Concat height width column into one colum for grouping DF by
    df["img_height_width"] = df["img_height"].astype(str) + "_" + df["img_width"].astype(str)
    grouped_df = df.groupby(['img_height_width']).size().reset_index(name='size')
    # Get the largest group of images with the same height & width
    largest_group = grouped_df.loc[grouped_df['size'].idxmax()]
    largest_subset_df = df.loc[df.img_height_width == largest_group['img_height_width']]

    return grouped_df, largest_subset_df

def show_scatter_plot(df):
    # plot scatter plot of image dimensions
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111)
    points = ax.scatter(df.img_width, df.index, color='blue', alpha=0.5, s=df["aspect_ratio"]*100, picker=True)
    ax.set_title("Image Resolution")
    ax.set_xlabel("width", size=14)
    ax.set_ylabel("height", size=14)
    plt.show()


def plot_hist(df):
    # Plot hist of count of images grouped by image dimensions
    ax = df.plot.bar(x = "height_width_dims", y = "size", alpha=0.5)
    plt.show()


def segmment_dataset_by_img_dims(img_data_df, grouped_df):

    size_path = "size_segmented_dataset/"
    create_folder(size_path)
    # Get unique cols that the other DF doesn't have
    cols_to_use = img_data_df.columns.difference(grouped_df.columns)
    df = pd.merge(img_data_df[cols_to_use], grouped_df, how='outer', on = "id")

    sizes = list(df['height_width_dims'].unique())
    for height_width in sizes:
        img_folder_path = str(size_path) + height_width + "/"
        create_folder(img_folder_path)
        # Select query for DF
        df_subset = df[df["height_width_dims"] == height_width]
        # for img_name in df.index
    

def get_dataset_pc_classified(json_path, dataset_path):
    # Get stored dataset class results
    json_data = import_json(json_path)

    ids = list(json_data.keys())
    class_results = list(json_data.values())
    dataset_size = len(ids)

    # Calculate % of dataset thats been completed 
    print("Current length =", dataset_size - 1)
    print("% Done:", 100 * (dataset_size/len(os.listdir(dataset_path))))


def create_test_dataset(largest_subset_df, dataset_path, test_folder_path):
    """
    """
    create_folder(test_folder_path)
    for image_name in largest_subset_df.index:
        src_path = dataset_path + image_name
        dest_path = test_folder_path + image_name

        print(src_path)
        if os.path.isfile(src_path):
            shutil.copyfile(src_path, dest_path)


def get_test_set_results(df, json_path):
    """ Extract classifications for each ID in the df
    Args:
        df (DataFrame) : DataFrame containing all the ID's whos classifications arre to be extracted
        json_path (String) : A string to the JSON file containing all of our classifications

    Returns:

    """
    json_class_data = import_json(json_path)
    subset_json_classifications = dict((k, json_class_data[k]) for k in df.index)
    subset_df = pd.DataFrame(subset_json_classifications.items())
    subset_df.columns = ['id', 'class']
    subset_df.set_index('id', inplace=True)

    counts_df = subset_df.groupby(['class']).size().reset_index(name='count')
    print(counts_df)

    return subset_df

def main():

    create_folder("csv/")

    # Load image DF if its been made previously
    path = "csv/img_metadata.csv"
    json_path = "results.json"
    dataset_path = "clothes_dataset/"

    # Build image df if it has never been built before
    # metadata_df = build_img_df(dataset_path)

    # Load the image metadata DataFrame
    df = get_img_data_df(path)

    # Calculates what percentage of the dataset has been annotated 
    # get_dataset_pc_classified(json_path, dataset_path)
    # segmment_dataset_by_img_dims(df, grouped_df)

    grouped_df, largest_subset_df = get_grouped_df(df)

    test_set = "test_set/"
    test_folder_path = test_set  + dataset_path  
    create_folder(test_set)
    create_folder(test_folder_path)
    testset_results = get_test_set_results(largest_subset_df, json_path)
    # create_test_dataset(largest_subset_df, dataset_path, test_folder_path)

    print("LENGTH OF SET:", len(os.listdir(test_folder_path)))

    # Plot the different image dimensions as a scatter plot to see level of disparity & bar chart for volume
    # visualise_img_metadata(df, grouped_df)

if __name__ == "__main__":
    main()