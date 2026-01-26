from bs4 import BeautifulSoup
import requests
import re

class Book:
    def __init__(self, title, price, rating, availability, upc, description):
        self.title = title
        self.price = self.clean_price(price)
        self.rating = rating
        self.availability = self.clean_availability(availability)
        self.upc = upc
        self.description = description

    @staticmethod
    def clean_price(price):
        return float(price.replace(",", ".").replace("£", ""))

    @staticmethod
    def clean_availability(availability):
        return int(re.search(r'\d+', availability).group())

    def __repr__(self):
        return f"<Book: {self.title}, {self.price}£, {self.rating}, {self.availability}, {self.upc}>"



def deep_book_scraper(url):
    #TODO gestire eventuali URL mancanti
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    article = soup.find("article", class_="product_page")

    title = article.find("div", class_="col-sm-6 product_main").h1.get_text()
    price = article.find("p", class_="price_color").get_text()
    rating = article.find("p", class_="star-rating")["class"][1]
    description = article.find("p").get_text()

    table = article.find("table", class_="table")
    rows = table.find_all("tr")
    upc = table.find_all("td").text
    availability = rows[5].td.get_text()

    return Book(title = title,
                price = price,
                rating = rating,
                availability = availability,
                upc = upc,
                description = description)