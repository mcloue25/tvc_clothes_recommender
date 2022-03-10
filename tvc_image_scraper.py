import sys
import os
import json
import urllib
import shutil
import requests

from difPy import dif
from datetime import date
from bs4 import BeautifulSoup
from PIL import Image, ImageStat

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

# import numpy as np
# import cv2
# import imghdr

""" WEBSITES TO BE SCRAPED

    Donn Clothing:          https://donnclothing.com/shop/
    TVC Clothing:           https://wearetvc.com/
    TVC Asos MarketPlace:   https://marketplace.asos.com/boutique/tvc-vintage

"""

def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

def delete_folder(formatted_date):
    path = "tmp/" + formatted_date + "/"
    shutil.rmtree(path)


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
    page_url = base_url + str(page_no) + "/"
    # response = requests.get(page_url)
    # soup = BeautifulSoup(response.text, 'html.parser')
    # print(page_url) 
    
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

        # Removes the majority of logos from donnclothing.com
        if name == "DONN Clothing":
            print("Donn Clothing Logo")

        # else:
        #     print("SRC", src)
        #     print("name", name)

        # Clean the image URL so that it can used to download the image
        if 'https:' not in src:
            image_url = 'https:' + src.strip().split("?")[0]
        else:
            image_url = src.strip().split("?")[0]
        # Download the image
        img_data = requests.get(image_url).content
        # Creating a unique image identifier:  <<name>>_<<page_number>>_<<counter>>_<<date>>
        unique_image_identifier  = name.replace(" ", "_").lower() + "_" + str(page_no).replace("/", "") + "_" + str(counter) + "_" + date + ".jpg"
        # Get the folder name based on the date
        folder_name = "tmp/" + date + "/"  
        counter +=1
        # Save the downloaded image to the created date folder
        try:
            with open(folder_name + unique_image_identifier, 'wb') as handler:
                handler.write(img_data)
                print("SAVED:", folder_name + unique_image_identifier)
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


def check_for_duplicates(folder_path):
    """ Checks for duplicate files in the folder path provided
        Once any/all duplicates have been identified, all unique images are moved to clothes_dataset/
    Args:
        folder_path (String) : A string file path to the folder we want to check for duplicates in
        
    """
    # Line where the folder is analysed for duplicates
    search = dif(folder_path, folder_path)
    # Convert the search result to a list containing all of the file paths to duplicate images in the folder
    duplicate_list = list(search.lower_quality)
    
    if duplicate_list:
        print("HERE", duplicate_list)
        duplicate_names = [i.split("/")[2] for i in duplicate_list]

        # Remove duplicate images from the dataset folder to a duplicate folder which will be deleted 
        for duplicate_uid in duplicate_names:
            src_path = folder_path + duplicate_uid
            try:
                os.remove(src_path)
        
            except:
                print("Couldn't :", duplicate_uid)

    return


def add_clothes_to_dataset(formatted_date):

    folder_path = "tmp/" + formatted_date + "/"
    images = os.listdir(folder_path)

    for image in images:
        src_path = folder_path + image
        dest_path = "clothes_dataset/" + image
        shutil.move(src_path, dest_path)

    return


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


def get_images_from_donn_clothing(formatted_date):
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

def scrape_tola_vintage(formatted_date):
    base_url = "https://www.tolavintage.com/men/?product-page="
    for page_no in range(1, 30):
        scrape_images_from_page(base_url, page_no, formatted_date)


def rename(formatted_date):
    path = "tmp/" + formatted_date + "/"
    images = os.listdir(path)
    for index, image_name in enumerate(images):
        src = path + image_name
        dest = path + "tola_vintage_" + str(index) + "_" + formatted_date + ".jpg"
        os.rename(src, dest)


def get_dataset_size(path):
    img_count = len(os.listdir(path))

    print("The current size of the dataset is", img_count)


def scrape_tvc_main():
    # Base folder that all of the clothes dataset will be stored in
    tmp_folder = "tmp/"
    clothes_dataset = "clothes_dataset/"
    
    # Get the current date and create a folder
    today = date.today() 
    formatted_date = today.strftime("%d_%m_%Y")
    folder_name = tmp_folder + formatted_date + "/"

    # Create the two folders needed for the preliminary scrapes and final dataset
    create_folder(clothes_dataset)
    create_folder(tmp_folder)
    create_folder(folder_name)
    
    # Runn web scrapers
    # get_images_from_wearTVC(formatted_date)
    # get_images_from_donn_clothing(formatted_date)
    # scrape_tola_vintage(formatted_date)

    # Remove any duplicate images from the dataset if they exist  clothes_dataset
    # check_for_duplicates("tmp/" + formatted_date)

    # rename(formatted_date)
    # Move scraped images to the clothes dataset
    # add_clothes_to_dataset(formatted_date)

    # Get the size of the current dataset
    get_dataset_size(clothes_dataset)

    # delete_folder(formatted_date)


if __name__ == "__main__":
    scrape_tvc_main()


"""
    Notes: 
    Link : https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&as_vis=1&q=personalized+garment+design+fashion+recommender+system&oq=fashion+recommender+system
"""