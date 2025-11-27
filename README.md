# price_extraction
Scraping books from https://books.toscrape.com/  : extracting data, transforming and saving in CSV and uploading images.

## Description 
This project allows you to :
- Extract information from books (URL, UPC, title, prices (with and without tax), number available, product description, category, review rating).
- Save the data into separate csv files organized by category (into courant folder "files_csv")
- Download book images into folders organized by category (into courant folder "pictures")
- Handle errors using the `execute_safely` safety function.

## Installation
1) Clone the repository : https://github.com/Nasunaj/price_extraction.git  
2) Create a virtual environment
3) Install the dependencies : ```pip install -r requirements.txt```

## Project structure
```
├── main.py
├── README.md
├── requirements.txt
└── scraper
    ├── errors.py
    ├── extraction.py
    ├── __init__.py
    ├── load.py
    └── transformation.py
```

## Usage
` python3 path_your_project/main.py
`