import sys
import os
import json
import urllib
import shutil
import requests
import hashlib

from datetime import date
from bs4 import BeautifulSoup

from PIL import Image, ImageStat

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import skimage.measure
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import imghdr

#To search for duplicates within two folders:

from difPy import dif

# https://donnclothing.com/shop/page/3/?product-cato=196


def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)


def get_last_page_number(base_url, page_class):
    # List to store all pages that we will examine
    page_numbers = []
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Get all pages displayed at the bottom of the screen
    pagination = soup.find('ul', class_=page_class)
    for href in pagination.find_all('a', href=True):
        if href.text.isnumeric():
            page_numbers.append(href.text)

    # last_page_no = max([href for href in pagination.find_all('a', href=True) if href.text.isnumeric()])
    
    return max(page_numbers)


def scrape_images_from_page(base_url, page_no, date):
    """ Used to download all of the images from a given web page.
        Each image will have a unique identifier created for it of <<ITEM_NAME>>_<<PAGE_NUMBER>>_<<DATE>>
    Args:
        base_url (List) : A String URL of the page containing all of the images you want to download
        page_no (String) : A String representing the current page being looked at
        date (String) : The current date in the format: DD_MM_YYYY
        
    """
    headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
    }

    # Creating the URL for each page 
    page_url = base_url + page_no + "/"
    # response = requests.get(page_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    print(page_url) 
    
    response = requests.get(page_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # print("URL:", page_url)
    # Collect all images from the page
    counter = 0
    for image in soup.findAll('img'):
        # Get the image data-src and name
        src = image.get('src', image.get('dfr-src'))
        name = image.get('alt', image.get('alt'))
        # Check if there is a source
        if src is None:
            continue 

        print("SRC", src)
        print("name", name)
        # Clean the image URL so that it can used to download the image
        # image_url = 'https:' + src.strip().split("?")[0]
        image_url = src.strip().split("?")[0]
        print("IMAGE_URL", image_url)
        # Download the image
        img_data = requests.get(image_url).content
        # Creating a unique image identifier 
        unique_image_identifier  = name.replace(" ", "_").lower() + "_" + page_no.replace("/", "") + "_" + date + ".jpg"
        uid  = str(page_no) + "_" + str(counter) + ".jpg"
        # Get the folder name based on the date
        folder_name = "tmp/" + date + "/"  
        counter +=1
        print("BOTH:", folder_name + unique_image_identifier)
        # Save the downloaded image to the created date folder
        try:
            with open(folder_name + uid, 'wb') as handler:
                handler.write(img_data)
                print("Saved:", folder_name + uid)
                print()

        except Exception as e:
            print(e)
            print("Couldnt save " + unique_image_identifier)
            print()



def scrape_all_clothes_images(base_url, page_no, date):
    """
        need to get all hrefs inside div products producrs-grid
        get the name of the clothes in each box as well as the href 
        follow that href and then use the original scrape_images() to get all angles of each clothes item 
        save these images to tmp/date/item_name/<< HERE >>

    """
    page_url = base_url + str(page_no)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # List to store all product ID's on the page 

    divTag = soup.find_all("div", {"class": "product product-grid"})
    # Collect all images from the page
    # for image in soup.findAll('img'):


def check_for_duplicates():
    """ Checks for duplicate files in the folder path provided
        Once any/all duplicates have been identified, all unique images are moved to clothes_dataset/
    Args:
        path (String) : A string of the file path to be evaluated
        
    """
    # Dicts to store the image ID's & pixel mean as well as their image ID's & the folder theyre contained in
    duplicates_list = dif("clothes_dataset/", "clothes_dataset/")
    print()
    if duplicates_list:
        dup_folder = "duplicates/"
        create_folder(dup_folder)
        # print(duplicates.lower_quality)
        for duplicate_path in duplicates_list:
            print(duplicate_path)



def add_clothes_to_dataset(new_clothes_items, formatted_date):

    for item in new_clothes_items:
        src = "tmp/" + formatted_date + "/" + item
        # print("SRC:", src)
        dest = "clothes_dataset/" + item
        shutil.move(src, dest)


def get_images_from_wearTVC(formatted_date):
    """ Creates a segmented video using the frame indexes provided in frames
    Args
        parent_frame_folder_path (String) : A string indicating the parent folder of all frames Eg. "video_frames/<<video_name>>/"
    Returns:
        parent_frame_folder_path (String) : A string indicating the parent folder of all frames Eg. "video_frames/<<video_name>>/"
    """
    # Hard code way of collecting the last number in the list 
    base_url = 'https://wearetvc.com/collections/all?page='
    page_one_url = base_url + "1"
    page_class = 'pagination'
    # Find out how many pages we have to iterate over
    total_pages = get_last_page_number(page_one_url, page_class)
    # Iterate through each page and save images to tmp folder 
    for i in range(1, int(total_pages) + 1):
        scrape_images_from_page(base_url, str(i), formatted_date)

    # Create pixel maps for the clothes dataset and the newly scraped clothes
    new_folder = "tmp/" + formatted_date + "/"
    # dataset_map = create_pixel_map("clothes_dataset/") 
    # new_data_map = create_pixel_map(new_folder)

    # new_clothes_items = compare_map_values(dataset_map, new_data_map)

    # add_clothes_to_dataset(new_clothes_items, formatted_date)


def get_images_from_asos_marketplace(formatted_date):
    # base_url = "https://marketplace.asos.com/boutique/tvc-vintage#pgno="
    base_url = "https://donnclothing.com/shop/page/"
    page_one_url = base_url + "1"
    # Find out how many pages we have to iterate over
    page_class = 'nav'
    # total_pages = get_last_page_number(page_one_url, page_class)
    total_pages = 14
    # Iterate through each page and save images to tmp folder 
    for i in range(1, total_pages):
        page_no = str(i)
        # Need to creatr UID of PAGENUMBER_COUNTER
        scrape_images_from_page(base_url, page_no, formatted_date)
        # scrape_images_from_page(base_url, str(i), formatted_date)


def get_dataset_size(path):
    img_count = len(os.listdir(path))

    print("The current size of the dataset is", img_count)


def scrape_tvc_main():
    # Base folder that all of the clothes dataset will be stored in
    tmp_folder = "tmp/"
    clothes_dataset = "clothes_dataset/"
    f = tmp_folder + "19_02_2022/"
    create_folder(clothes_dataset)
    create_folder(tmp_folder)
    # Get the current date and create a folder
    today = date.today() 
    formatted_date = today.strftime("%d_%m_%Y")
    folder_name = tmp_folder + formatted_date + "/"
    create_folder(folder_name)
    
    # get_images_from_wearTVC(formatted_date)
    # get_images_from_asos_marketplace(formatted_date)
    # Now check if any duplicates exist in our dataset
    # check_for_duplicates(tmp_folder)
    # get_clothes_dataset_pixel_map(clothes_dataset)

    # check_for_duplicates("tmp/")

    
    get_dataset_size(clothes_dataset)
    get_dataset_size(f)

    check_for_duplicates()

    # upload_to_google_drive(folder_name)


if __name__ == "__main__":
    scrape_tvc_main()


"""
    Notes: 
    Link : https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_vis=1&q=personalized+garment+design+fashion+recommender+system&oq=fashion+recommender+system
"""