import os
import urllib
import shutil
import requests
from datetime import date
from bs4 import BeautifulSoup

import collections


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



def scrape_tvc_main():

    today = date.today()
    print("Today's date:", today)

    # Get the current date and create a folder 
    formatted_date = today.strftime("%d_%m_%Y")
    folder_name = formatted_date + "/"
    create_folder(folder_name)

    # Hard code way of collecting the last number in the list 
    base_url = 'https://wearetvc.com/collections/all?page='

    page_one_url = base_url + "1"
    
    # Find out how many pages we have to iterate over
    total_pages = get_last_page_number(page_one_url)

    # product_ids = []
    for i in range(1, int(total_pages) + 1):
        scrape_images_from_page(base_url, str(i), formatted_date)
        # product_ids = product_ids + downloaded_product_ids

    # print(product_ids)
    # print("DUPLICATES:")
    # print([item for item, count in collections.Counter(product_ids).items() if count > 1])


if __name__ == "__main__":
    scrape_tvc_main()
