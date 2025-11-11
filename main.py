import time
import random
import csv
import scraper.scraper as scr

def main():
    pages_ = scr.url_des_pages()
    '''
    for page_url in pages_:
        url_books = url_book_f(url_de_la_page=page_url)
        for url_book in url_books:
            dict_one_book = data_book(url_book_i=url_book)
            list_data_livre.append(dict_one_book)
        #Random pause from 0.5 to 2 seconds to avoid being detected as a bot
        time.sleep(random.uniform(0.5, 2))
    '''

    colonnes = ["product_page_url", "universal_ product_code", "title", "price_including_tax", "price_excluding_tax",
                "number_available",
                "product_description", "category", "review_rating", "image_url"]  # ordre voulu dans le CSV

    with open("books.csv", mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=colonnes)
        writer.writeheader()
        for page_url in pages_:
            urls_books = scr.url_book_f(url_de_la_page=page_url)
            for url_book in urls_books:
                try:
                    data = scr.data_book(url_book_i=url_book)
                    writer.writerow(data)
                except Exception as e:  # capte tout type d'erreur
                    print(f"erreur {e} url {url_book}")
                    continue
                time.sleep(random.uniform(0.5, 1.5))




if __name__ == "__main__":
    main()


