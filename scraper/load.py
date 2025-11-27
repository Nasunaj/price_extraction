import csv
import logging
import os
from .extraction import categories_gen, pages_categorie_gen, livres_page_gen
from .transformation import data_book
from .errors import execute_safely
'''
from scraper.scraper2 import categories_gen, pages_categorie_gen, livres_page_gen
from scraper.databook import data_book
from scraper.errors import execute_safely
'''

def scrap_site(home_url):
    """.CSV for each categories, one book per ligne."""

    # create the files
    os.makedirs("files_csv", exist_ok=True)
    os.makedirs("pictures", exist_ok=True)


    for categorie_name, categorie_url in categories_gen(home_url):
        seen_books = set()  # I don't know why, There was a duplicate problem, so I added set() to don't processed 2 same url. put here for each category.
        filename = os.path.join("files_csv",f"{categorie_name}.csv")
        logging.info(f"Scraping catégorie '{categorie_name}' : {filename}")

        folder_path = os.path.join("pictures", f"{categorie_name}")  # folder by category as csv in scrap_site else don't work
        os.makedirs(folder_path, exist_ok=True)  # create folder


        try:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=[
                    "product_page_url", "universal_product_code", "title",
                    "price_including_tax", "price_excluding_tax", "number_available",
                    "product_description", "category", "review_rating", "image_url"
                ])
                writer.writeheader()

                for page_soup in pages_categorie_gen(categorie_url):
                    for url_book in livres_page_gen(page_soup, categorie_url):
                        if url_book in seen_books:
                            continue #ignore if already processed
                        seen_books.add(url_book) #Add as processed

                        book_data = execute_safely(data_book, url_book)
                        if book_data:#if book_data ok not None write in csv and upload pictures
                            # Filter only the keys in writer.fieldnames
                            filtered_data = {}
                            for k in writer.fieldnames:
                                filtered_data[k] = book_data[k]
                            execute_safely(writer.writerow,filtered_data)
                            print(f"data load for : {url_book}")
                            if book_data["image_url"]:
                                try :
                                    image_filename = os.path.join(folder_path, book_data["image_url"].split("/")[-1])  # we want the last element name.jpg
                                    with open(image_filename, "wb") as f:
                                        f.write(book_data["img_response"].content)  # write the content
                                    print(f"picture ({book_data['image_url']}) download : {image_filename}")
                                except Exception :
                                    print(f"Impossible to download the picture {url_book}")
                        else:
                            print(f"data not loaded for : {book_data}")
        except Exception as e:
            logging.warning(f"CSV write error for {categorie_name} : {e}")