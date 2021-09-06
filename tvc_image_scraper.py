import re
import urllib
import shutil
import requests
from bs4 import BeautifulSoup

def get_last_page_number(base_url):

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup)

    div = soup.find("div", {"id": "collection-footer"})
    print("base_url", base_url)
    print("HERE", div)

    # web_page = base_url + str(page_counter)

    # print("web_page", web_page)

    # try:
    #     response = requests.get(web_page)
    #     print("URL is valid and exists on the internet")
    #     page_counter+=1
    #     get_last_page_number(base_url, page_counter)

    # except requests.ConnectionError as exception:
    #     return page_counter



def scrape_images_from_page(page_url):
    """ Used to download all of the images from a given web page.
        All of the downloaded images will then be saved as their names on the website 
    Args:
        page_url (List) : A String URL of the page containing all of the images you want to download
        
    """
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Collect all images from the page
    for image in soup.findAll('img'):
        # Get the image data-src and name
        src = image.get('src', image.get('dfr-src'))
        name = image.get('alt', image.get('alt'))

        if src is None:
            continue 
        # Clean the image URL so that it can used to download the image
        image_url = 'https:' + src.strip().split("?")[0]
        # print("Name:", name)
        # print("SRC:", src)
        # print()

        # Download the image
        # img_data = requests.get(image_url).content
        # image_name = name + '.jpg'
        # # Save the downloaded image to the clothes folder
        # with open('clothes/' + image_name, 'wb') as handler:
        #     handler.write(img_data)


"""
iterate over every page of shop URL
save the original name of the image as well as give it a new coded image EG 0_M , 1_36W_34L
create JSON file that can be updated for the countrer as all these codes


"""

def scrape_tvc_main():


    # Need a way to know how many pages are in the collection
    page_counter = 1
    # Hard code way of collecting the last number in the list 
    base_url = 'https://wearetvc.com/collections/all?page=1'
    
    # Find out how many pages we have to iterate over
    total_pages = get_last_page_number(base_url)


    scrape_images_from_page(base_url)


if __name__ == "__main__":
    scrape_tvc_main()

 

#  ━━-╮
# ╰┃ ┣▇━▇
#  ┃ ┃  ╰━▅╮
#  ╰┳╯ ╰━━┳╯E Z A F
#   ╰╮ ┳━━╯T Y 4
#  ▕▔▋ ╰╮╭━╮ T U T O R I A L
# ╱▔╲▋╰━┻┻╮╲╱▔▔▔╲
# ▏  ▔▔▔▔▔▔▔  O O┃
# ╲╱▔╲▂▂▂▂╱▔╲▂▂▂╱
#  ▏╳▕▇▇▕ ▏╳▕▇▇▕
#  ╲▂╱╲▂╱ ╲▂╱╲▂   