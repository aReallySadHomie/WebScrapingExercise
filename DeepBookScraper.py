from bs4 import BeautifulSoup
import requests


def deep_book_scraper(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")