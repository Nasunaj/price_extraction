import requests
import os
from urllib.parse import urljoin
from .errors import execute_safely
from .scraper2 import html_parse

def data_book(url_book_i):
    """Retrieves information you want from your book's page."""
    soup = execute_safely(html_parse, url_book_i) #to control some possibilities error
    if soup is None:
        return None

    try:
        ul = soup.find("ul", class_="breadcrumb")
        li = ul.find_all("li")
        category = li[-2].get_text(strip=True)
        title = li[-1].get_text(strip=True)
    except :
        category = ""
        title = ""

    try:
        desc_div = soup.find("div", id="product_description")
        description = desc_div.find_next("p").get_text(strip=True)
    except Exception:
        description = ""

    try:
        table = soup.find("table")
        rows = table.find_all("tr")
        upc = rows[0].find("td").get_text(strip=True)
        price_excl = rows[2].find("td").get_text(strip=True)
        price_incl = rows[3].find("td").get_text(strip=True)
        available = rows[5].find("td").get_text(strip=True)
        rating = rows[6].find("td").get_text(strip=True)
    except Exception :
        upc = ""
        price_excl = ""
        price_incl = ""
        available = ""
        rating = ""

    try:
        img_tag = soup.select_one("div.item.active img")
        if img_tag:
            image_url = urljoin(url_book_i, img_tag["src"])
            # pictures________
            # create folder and extention
            folder_path = os.path.join("pictures", category) # folder by category as csv in scrap_site else don't work
            os.makedirs(folder_path, exist_ok=True) # create folder
            image_filename = os.path.join(folder_path, image_url.split("/")[-1]) #we want the last element name.jpg

            #downlod
            img_response = requests.get(image_url) #sends an HTTP GET request to the image URL. The server responds with: HTTP code (200, 404, 500...) Headers (Content-Type, Content-Length, etc.) the raw content (in this case, the bytes of the image)
            img_response.raise_for_status() #control error if error break
            with open(image_filename, "wb") as f:
                f.write(img_response.content) #write the content

            print(f"picture ({image_url}) download : {image_filename}")
        else:
            image_url = ""
            print(f"picture not found {url_book_i}")

    except Exception:
        image_url = ""
        print(f"Impossible to download the picture {url_book_i}")


    return {
        "product_page_url": url_book_i,
        "universal_product_code": upc,
        "title": title,
        "price_including_tax": price_incl,
        "price_excluding_tax": price_excl,
        "number_available": available,
        "product_description": description,
        "category": category,
        "review_rating": rating,
        "image_url": image_url
    }
