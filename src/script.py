# Importing Python packaging
import re
import requests
from bs4 import BeautifulSoup

'''
C'est un Brouillon ==> par la suite faire des modules et fonctions et faire appel dans __main__
en arrivant sur la page principale l'ensemble des livres sont répertoriés sur 50 pages web :
1) Récupérer le nombre de page total :cohérence 1ère age index.html puis indexation à partir de 2
    2) pour chaque page récuprer dans une liste l'ensemble des livres
        3) pour chaque livre récuérer l'ensemble des éléments dans un dictionnaire (un dictionnaire par livre)
        4) faire une liste de l'ensemble des dictionnaire
        4 exporter csv (une ligne avec l'ensemble des information')
'''

#--------------Brouillon : décomposition du code pour arriver à extraire les information pour un livre-----------------

#url de la page générale, récupére html de la page
url="https://books.toscrape.com" #saving the url
page=requests.get(url)
soup=BeautifulSoup(page.content,"html.parser")

'''
#pour mieux comprendre la page, j'exporte la page html
with open("page_scraping.html", "wb") as f:
    f.write(page.content)
'''

#les liens en fonction des themes ici pas nécessaire car l'ensemble des livres se trouve sur le lien books_1
#seulement coserver le 1er lien de la liste
links = soup.select('ul.nav.nav-list a')
hrefs_theme = []
for link in links:
    hrefs_theme.append(f"{url}/{link.get('href')}")

page2=requests.get(hrefs_theme[0])
soup2=BeautifulSoup(page2.content,"html.parser")
'''
with open("page2_scraping.html", "wb") as f:
    f.write(page2.content)
'''
#Pour récupérer le nombre de page total :  le dernier nombre de la page
current = soup2.find("li", class_="current")
current=current.get_text(strip=True)
numbers=re.findall(r'\d+',current)
total_pages=int(numbers[-1])


#pour naviguer entre les pages : on récupére le lien des pages
nb_page_link=soup2.find("li", class_="next").find("a").get("href")
list_page_link_without_number=re.split(r'(\d+)',nb_page_link)
list_nb_page_link=[]
#sans après le dernier slash
last_slash = hrefs_theme[0].rfind("/")
url_without_after_last_slash=hrefs_theme[0][:last_slash+1]
for i in range (1,total_pages):
    if i==1:
        list_nb_page_link.append(hrefs_theme[0])
    else:
        new_part_link_page=f"{list_page_link_without_number[0]}{i}/{list_page_link_without_number[-1]}"
        new_url=f"{url_without_after_last_slash}{new_part_link_page}"
        list_nb_page_link.append(new_url)



# Touver le lien pour chaque livre titre h3 href
url_page_ind=list_nb_page_link[0]
page_ind=requests.get(url_page_ind)
soup_page_ind=BeautifulSoup(page_ind.content,"html.parser")
url_book=soup_page_ind.select("h3 a")
list_href_url_book = []
for link in url_book:
    list_href_url_book.append(f"{url}/{link.get('href').replace("../..", "catalogue")}")



#----recupere donnees pour chaque livre------
url_book_i=list_href_url_book[0]
page_book_i=requests.get(url_book_i)
soup_page_book_i=BeautifulSoup(page_book_i.content,"html.parser")
with open("book_scraping.html", "wb") as f:
    f.write(page_book_i.content)
ul_book_i=soup_page_book_i.find("ul",class_="breadcrumb")
#récuére tous les li
li_theme_book_i = ul_book_i.find_all("li")
theme_i=li_theme_book_i[-2].get_text(strip=True)
titre_i=li_theme_book_i[-1].get_text(strip=True)

#description
div_descript_book_i = soup_page_book_i.find("div", id="product_description")
#paragraph suivant
p_after_div_descipt_book_i = div_descript_book_i.find_next("p").get_text(strip=True)

#les éléments de la tables
table_book_i=soup_page_book_i.find("table")
table_ti_book_i=table_book_i.find_all("tr")
#upc
upc_book_i=table_ti_book_i[0].find("td").get_text(strip=True)
#price_excluding_tax
price_excluding_tax_book_i=table_ti_book_i[2].find("td").get_text(strip=True)
#price_including_tax
price_including_tax_book_i=table_ti_book_i[3].find("td").get_text(strip=True)
#number_available
number_available_book_i=table_ti_book_i[5].find("td").get_text(strip=True)
#review_rating
review_rating_book_i=table_ti_book_i[6].find("td").get_text(strip=True)

#image url
image_url_book_i=soup_page_book_i.find("img").get("src").replace("../..","")
dict_book_i = {
    "product_page_url":url_book_i,
    "universal_ product_code":upc_book_i,
    "title": titre_i,
    "price_including_tax": price_including_tax_book_i,
    "price_excluding_tax": price_excluding_tax_book_i,
    "number_available": number_available_book_i,
    "product_description":p_after_div_descipt_book_i,
    "category": theme_i,
    "review_rating": review_rating_book_i,
    "image_url":f"{url}{image_url_book_i}"
}
print(dict_book_i)



