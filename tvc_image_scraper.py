import os
import urllib
import shutil
# import hashlib
import requests
from datetime import date
from bs4 import BeautifulSoup

from PIL import Image, ImageStat

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def get_last_page_number(base_url):
    # List to store all pages that we will examine
    page_numbers = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get all pages displayed at the bottom of the screen
    pagination = soup.find('ul', class_='pagination')
    for href in pagination.find_all('a', href=True):
        if href.text.isnumeric():
            page_numbers.append(href.text)
    # print("page_numbers", page_numbers)
    return max(page_numbers)




def scrape_images_from_page(base_url, page_no, date):
    """ Used to download all of the images from a given web page.
        Each image will have a unique identifier created for it of <<ITEM_NAME>>_<<PAGE_NUMBER>>_<<DATE>>
    Args:
        base_url (List) : A String URL of the page containing all of the images you want to download
        page_no (String) : A String representing the current page being looked at
        date (String) : The current date in the format: DD_MM_YYYY
        
    """
    # Creating the URL for each page 
    page_url = base_url + str(page_no)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # List to store all product ID's on the page 

    # Collect all images from the page
    for image in soup.findAll('img'):
        # Get the image data-src and name
        src = image.get('src', image.get('dfr-src'))
        name = image.get('alt', image.get('alt'))
        # Check if there is a source
        if src is None:
            continue 

        # Clean the image URL so that it can used to download the image
        image_url = 'https:' + src.strip().split("?")[0]

        # Download the image
        img_data = requests.get(image_url).content
        # Creating a unique image identifier 
        unique_image_identifier  = name.replace(" ", "_").lower() + "_" + page_no + "_" + date + ".jpg"
        # Get the folder name based on the date
        folder_name = date + "/"   
        # Save the downloaded image to the created date folder
        try:
            with open(folder_name + unique_image_identifier, 'wb') as handler:
                handler.write(img_data)

        except:
            print("Couldnt save " + unique_image_identifier)



# def upload_to_google_drive(folder_name):


def check_for_duplicates(path):
    # Dicts to store the image ID's & pixel mean as well as their image ID's & the folder theyre contained in
    parent_map = {}
    folder_dict = {}
    folders = os.listdir(path)
    for folder in folders:
        # Get path to each folder and list of images it contains
        folder_path = path  + folder + "/"
        image_list = os.listdir(folder_path)
        for image in image_list:
            # Get the path to the image and create a hashcode and add it to the map
            image_path = folder_path + image
            image_org = Image.open(image_path)
            pix_mean = ImageStat.Stat(image_org).mean
            # Save pixel mean to map with the image identifier as its key
            parent_map[image] = pix_mean
            # Save image name as key & folder
            folder_dict[image] = folder

    # Save all pixel means to a list to identify duplicate values
    img_vals = list(parent_map.values())
    duplicate_vals = [x for i, x in enumerate(img_vals) if img_vals.count(x) > 1]
    # Dictionary containing no duplicates
    cleaned_dict = {key:val for key, val in parent_map.items() if val not in duplicate_vals}

    # Find what folder each of the unique ID's are contained in and copy them to the cleaned folder
    unique_images = list(cleaned_dict.keys())
    for image_name in unique_images:
        folder = folder_dict[image_name]
        src = "tmp/"+ folder + "/" + image_name
        dest = "clothes_dataset/" + image_name
        shutil.move(src, dest)


def get_images_from_wearTVC(formatted_date):
    """ Creates a segmented video using the frame indexes provided in frames
    Args:
        parent_frame_folder_path (String) : A string indicating the parent folder of all frames Eg. "video_frames/<<video_name>>/"
    Returns:
        parent_frame_folder_path (String) : A string indicating the parent folder of all frames Eg. "video_frames/<<video_name>>/"
    """
    # Hard code way of collecting the last number in the list 
    base_url = 'https://wearetvc.com/collections/all?page='
    page_one_url = base_url + "1"
    # Find out how many pages we have to iterate over
    total_pages = get_last_page_number(page_one_url)
    product_ids = []
    for i in range(1, int(total_pages) + 1):
        scrape_images_from_page(base_url, str(i), formatted_date)


def get_dataset_size(path):
    img_count = len(os.listdir(path))

    print("The current size of the dataset is", img_count)


def scrape_tvc_main():
    # Base folder that all of the clothes dataset will be stored in
    tmp_folder = "tmp/"
    clothes_dataset = "clothes_dataset/"
    create_folder(clothes_dataset)
    create_folder(tmp_folder)
    # Get the current date and create a folder
    today = date.today() 
    formatted_date = today.strftime("%d_%m_%Y")
    folder_name = tmp_folder + formatted_date + "/"
    create_folder(folder_name)
    
    # get_images_from_wearTVC(formatted_date)
    # Now check if any duplicates exist in our dataset
    # check_for_duplicates(tmp_folder)
    
    get_dataset_size(clothes_dataset)

    # upload_to_google_drive(folder_name)

    # print(product_ids)
    # print("DUPLICATES:")
    # print([item for item, count in collections.Counter(product_ids).items() if count > 1])


if __name__ == "__main__":
    scrape_tvc_main()
