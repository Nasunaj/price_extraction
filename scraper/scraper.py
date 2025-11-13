# Importing Python packaging
import re
import requests
from bs4 import BeautifulSoup


def html_parse(url_="https://books.toscrape.com"):
    """
    This function returns a dictionary with the entered URL and the parsed HTML page.
    """
    url = url_  # saving the url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return {'url':url,'soup':soup}

# Links by theme are not necessary here because all the books are available at the books_1 link
# Only keep the first link from the list
def list_url_category_book(url=html_parse()["url"],soup_=html_parse()["soup"],select_='ul.nav.nav-list a',get_='href'):
    """
This function collects in a list all the URLs associated with each book category.
It takes the following input parameters:
- soup_: the parsed HTML page
- select_: the HTML tags to focus on
- get_: the HTML tag from which the last part of the URL is retrieved
The function returns a list.
    """
    links=soup_.select(select_)
    hrefs_theme=[]
    for link in links:
        hrefs_theme.append(f"{url}/{link.get(get_)}")
    return hrefs_theme




# To get the total number of pages: the last number on the page
def nb_page_tot(soup_category=html_parse(url_=list_url_category_book()[0])["soup"],balise_="li",class_balise="current") :
    current = soup_category.find(balise_, class_=class_balise)
    current=current.get_text(strip=True)
    numbers=re.findall(r'\d+',current)
    total_pages=int(numbers[-1])
    return total_pages


# To navigate between pages: we retrieve the page links
def url_des_pages(soup_category=html_parse(url_=list_url_category_book()[0])["soup"],hrefs_theme=list_url_category_book(),total_pages=nb_page_tot()) :
    nb_page_link=soup_category.find("li", class_="next").find("a").get("href")
    list_page_link_without_number=re.split(r'(\d+)',nb_page_link)
    list_nb_page_link=[]
    #sans après le dernier slash
    last_slash = hrefs_theme[0].rfind("/")
    url_without_after_last_slash=hrefs_theme[0][:last_slash+1]
    for i in range (1,total_pages+1):
        if i==1:
            list_nb_page_link.append(hrefs_theme[0])
        else:
            new_part_link_page=f"{list_page_link_without_number[0]}{i}{list_page_link_without_number[-1]}"
            new_url=f"{url_without_after_last_slash}{new_part_link_page}"
            list_nb_page_link.append(new_url)
    return list_nb_page_link



# Find the link for each book: title in h3 href
def url_book_f(url_de_la_page=url_des_pages()[0],url=html_parse()["url"]) :
    url_page_ind=url_de_la_page
    page_ind=requests.get(url_page_ind)
    soup_page_ind=BeautifulSoup(page_ind.content,"html.parser")
    url_book=soup_page_ind.select("h3 a")
    list_href_url_book = []
    for link in url_book:
        list_href_url_book.append(f"{url}/{link.get('href').replace('../..', 'catalogue')}")
    return list_href_url_book



#----Retrieve data for each book------
def data_book(url_book_i=url_book_f()[0],url=html_parse()["url"]):

    soup_page_book_i = html_parse(url_=url_book_i)["soup"]

    ul_book_i = soup_page_book_i.find("ul", class_="breadcrumb")
    # Retrieve all the li
    li_theme_book_i = ul_book_i.find_all("li")
    theme_i = li_theme_book_i[-2].get_text(strip=True)
    titre_i = li_theme_book_i[-1].get_text(strip=True)
    #becarreful no description for the book The Bridge to Consciousness
    try :
        # description
        div_descript_book_i = soup_page_book_i.find("div", id="product_description")
        # next paragraph
        p_after_div_descipt_book_i = div_descript_book_i.find_next("p").get_text(strip=True)
    except:
        p_after_div_descipt_book_i=""

    # The elements of the table
    table_book_i = soup_page_book_i.find("table")
    table_ti_book_i = table_book_i.find_all("tr")
    # upc
    upc_book_i = table_ti_book_i[0].find("td").get_text(strip=True)
    # price_excluding_tax
    price_excluding_tax_book_i = table_ti_book_i[2].find("td").get_text(strip=True)
    # price_including_tax
    price_including_tax_book_i = table_ti_book_i[3].find("td").get_text(strip=True)
    # number_available
    number_available_book_i = table_ti_book_i[5].find("td").get_text(strip=True)
    # review_rating
    review_rating_book_i = table_ti_book_i[6].find("td").get_text(strip=True)

    # image url
    image_url_book_i = soup_page_book_i.find("img").get("src").replace("../..", "")
    dict_book_i = {
        "product_page_url": url_book_i,
        "universal_ product_code": upc_book_i,
        "title": titre_i,
        "price_including_tax": price_including_tax_book_i,
        "price_excluding_tax": price_excluding_tax_book_i,
        "number_available": number_available_book_i,
        "product_description": p_after_div_descipt_book_i,
        "category": theme_i,
        "review_rating": review_rating_book_i,
        "image_url": f"{url}{image_url_book_i}"
    }
    return dict_book_i