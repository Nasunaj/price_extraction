import csv
import logging
import os
from .scraper2 import categories_gen, pages_categorie_gen, livres_page_gen
from .databook import data_book
from .errors import execute_safely
'''
from scraper.scraper2 import categories_gen, pages_categorie_gen, livres_page_gen
from scraper.databook import data_book
from scraper.errors import execute_safely
'''

def scrap_site(home_url):
    """.CSV for each categories, one book per ligne."""

    # create the file
    os.makedirs("files_csv", exist_ok=True)

    for categorie_name, categorie_url in categories_gen(home_url):
        filename = os.path.join("files_csv",f"{categorie_name}.csv")
        logging.info(f"Scraping catégorie '{categorie_name}' → fichier {filename}")

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
                        book_data = execute_safely(data_book, url_book)
                        if book_data:#if book_data ok not None write in csv
                            execute_safely(writer.writerow, book_data)
        except Exception as e:
            logging.warning(f"Erreur écriture CSV pour {categorie_name} : {e}")