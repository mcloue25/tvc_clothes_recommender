# Author Eoin McLoughlin
import os
import bs4 as bs
import urllib.request
import lxml
import requests

from selenium import webdriver 
from selenium.webdriver.common.by import By

### GUIDE for getting the URL's ###
# https://www.youtube.com/watch?v=sMve66iaVQo
# https://www.youtube.com/watch?v=XRedIElqweI

### GUIDE for checking if downloadable ###



def get_images_selenium(url):
    browser = webdriver.Chrome("C:/Users/eoinm/Drivers/chromedriver")
    browser.get(url)
    request = requests.get(url)
    # Create a BeautifulSoup Object
    soup = bs.BeautifulSoup(request.text, "lxml")

    for image in soup.findAll('img'):
        # Get the image data-src and name
        src = image.get('src', image.get('dfr-src'))
        name = image.get('alt', image.get('alt'))
        # Check if there is a source
        if src is None:
            continue 

        print("Name:", name)

        

def open_soundcloud_browser():

    return browser


def chromdriver_main():
    
    get_images_selenium("https://www.depop.com/5975vintage/")

if __name__ == "__main__":
    chromdriver_main()