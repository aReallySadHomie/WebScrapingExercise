from turtledemo.paint import switchupdown
from unittest import case

from bs4 import BeautifulSoup
import requests
import re

class Book:
    def __init__(self, title, price, rating, availability, upc, description):
        self.title = title
        self.price = self.clean_price(price)
        self.rating = self.numeric_rating(rating)
        self.availability = self.clean_availability(availability)
        self.upc = upc
        self.description = description

    @staticmethod
    def clean_price(price):
        #TODO sistemare la regex per includere i punti e le virgole
        return float(re.search(r'(\d,)*\d+[,.]\d*', price).group())

    @staticmethod
    def clean_availability(availability):
        return int(re.search(r'\d+', availability).group())

    @staticmethod
    def numeric_rating(rating):
        match rating:
            case "One":
                return 1
            case "Two":
                return 2
            case "Three":
                return 3
            case "Four":
                return 4
            case "Five":
                return 5
        return 0

    def __repr__(self):
        return (f"Book: {self.title},\n"
                f"Price: {self.price}£,\n"
                f"Description: {self.description[:50]}...\n"
                f"Rating: {self.rating},\n"
                f"Availability: {self.availability},\n"
                f"UPC: {self.upc}\n")



def deep_book_scraper(url) -> Book:
    #TODO gestire eventuali URL mancanti
    response = requests.get(url, timeout=5)
    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find("article", class_="product_page")

    title = article.find("div", class_="col-sm-6 product_main").h1.get_text()
    price = article.find("p", class_="price_color").get_text()
    rating = article.find("p", class_="star-rating")["class"][1]
    description = article.find_all("p")[3].get_text() # hardcoded, non ne vado fiero

    table = article.find("table", class_="table")
    rows = table.find_all("tr")
    upc = rows[0].td.text
    availability = rows[5].td.get_text()

    return Book(title = title,
                price = price,
                rating = rating,
                availability = availability,
                upc = upc,
                description = description)