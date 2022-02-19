import json

import requests
from bs4 import BeautifulSoup

headers = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"
}

product_url = "https://marketplace.asos.com/boutique/tvc-vintage#pgno=10"
page = requests.get(product_url, headers=headers)
soup = BeautifulSoup(page.text, "html.parser")

for image in soup.findAll('img'):

        # Get the image data-src and name
        src = image.get('src', image.get('dfr-src'))
        name = image.get('alt', image.get('alt'))
        # Check if there is a source
        if src is None:
            continue 
        # print(name)
        print("SRC:", src)
        # Clean the image URL so that it can used to download the image
        image_url = 'https:' + src.strip().split("?")[0]
        # print(image_url)
        try:
        # Download the image
            img_data = requests.get(image_url).content
            print(img_data)
            # Creating a unique image identifier 
            unique_image_identifier  = name.replace(" ", "_").lower() + "_" + page_no + "_" + date + ".jpg"
            # Get the folder name based on the date
            folder_name = "tmp/" + date + "/"   
            # Save the downloaded image to the created date folder
            try:
                with open(folder_name + unique_image_identifier, 'wb') as handler:
                    handler.write(img_data)
                    print("Saved:", name)

            except:
                print("Couldnt save " + unique_image_identifier)
        except:
            print("Something went wrong downloading", name)


# print(product_data["name"], product_data["color"], product_data["productID"])


# price_endpoint = f"https://www.asos.com/api/product/catalogue/v3/stockprice?productIds={product_data['productID']}&store=COM&currency=GBP"

# print(requests.get(price_endpoint, headers=headers).json()[0]["productPrice"]["xrp"]["text"])