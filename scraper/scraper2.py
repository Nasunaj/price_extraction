import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from .errors import execute_safely

def html_parse(url="https://books.toscrape.com"):
    """
    This function returns a dictionary with the entered URL and the parsed HTML page.
    """
    page = requests.get(url,timeout=10)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup
'''
def html_parse(url):
    """Télécharge et parse une page HTML."""
    response = requests.get(url, timeout=10)
    return BeautifulSoup(response.text, "html.parser")
'''


def categories_gen(home_url):
    """
    with yield no need ta save in list as _url_category_book in scraper.py.
    This function stay open and process one by one the category link and the name

    """
    soup = execute_safely(html_parse, home_url)
    if soup is None:
        return

    try:
        book_link=soup.select_one('ul.nav-list > li> a') #without >li>a return list and we need to add [0] ==> soup.select('ul.nav-list li a')[0]
        book_url = urljoin(home_url, book_link.get('href'))
        book_name = book_url.rstrip("/").split("/")[-2]
        yield book_name, book_url
    except Exception as e:
        logging.warning(f"URL category book_1 error: {e}")

    links = soup.select('ul.nav-list ul li a')
    for link in links:
        try:
            categorie_url = urljoin(home_url, link.get('href'))
            categorie_name = categorie_url.rstrip("/").split("/")[-2] #rsplit delete the last slash then split and we take the second value from the end
            yield categorie_name, categorie_url
        except Exception as e:
            logging.warning(f"URL category error: {e}")



def pages_categorie_gen(categorie_url):
    """Generates all the pages of a category, true only for the 1st general category book."""
    page = 1
    while True:

        if page==1:
            url_page = categorie_url
        else:
            url_page = categorie_url.replace("index.html", f"page-{page}.html")
        soup = execute_safely(html_parse, url_page)
        '''
        url_page = categorie_url if page == 1 else categorie_url.replace("index.html", f"page-{page}.html")
        soup = execute_safely(html_parse, url_page)
        '''
        if soup is None: # is True exit the while loop
            break

        print(f"  → New page retrieved : {url_page}")
        yield soup

        try:
            livres_html = soup.select("article.product_pod a")
            if not livres_html:
                break
        except Exception as e:
            logging.warning(f"Erreur parsing livres sur {url_page}: {e}")
            break

        page += 1

def livres_page_gen(page_soup, categorie_url):
    """"Generates all the books url.."""
    try:
        livres_html = page_soup.select("article.product_pod a")
        for a in livres_html:
            yield urljoin(categorie_url, a['href'])
    except Exception as e:
        logging.warning(f"Erreur génération URL livres: {e}")
