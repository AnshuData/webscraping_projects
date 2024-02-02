import requests
from bs4 import BeautifulSoup
import time
import datetime
import csv
import pandas as pd
import re


def initialize_csv_file(filename="./files/price_check.csv", header=["book_title", "price", "date"]):
    """
    Initializes a CSV file with the given filename and writes the provided header into it.

    Args:
    - filename (str): The name of the CSV file to be initialized.
    - header (list): A list containing the header fields to be written into the CSV file.

    Returns:
    - None
    """
    with open(filename, "w", newline="", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)


import csv
import requests
from bs4 import BeautifulSoup
import re
import datetime

def price_check():
    """
    Checks the price of a product on a Walmart webpage and logs it along with the current date and time into a CSV file.
    """
    # URL of the product page to be checked
    URL = "https://www.walmart.com/ip/Percy-Jackson-and-the-Olympians-5-Book-Paperback-Boxed-Set-w-poster-Paperback-9781368098045/2041116385?athbdg=L1600"
    
    # Headers for the HTTP request
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1"
    }
    
    # Sending HTTP GET request to fetch the webpage content
    page = requests.get(URL, headers=headers)
    
    # Parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Extracting the title of the product
    title = soup.find(id='main-title').get_text()
    
    # Extracting the price of the product and formatting it
    price = soup.find(itemprop='price').get_text()
    price = re.sub('[a-zA-Z$]', "", price)
    price = price.strip()
    
    # Getting the current date and time
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Data to be written into the CSV file
    data = [title, price, date]
    
    # Appending the data to the CSV file
    with open("./files/price_check.csv", "a+", newline="", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(data)

price_check()

