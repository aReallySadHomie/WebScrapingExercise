import re

class Book:
    def __init__(self, title, price, rating, availability, upc, description, url):
        self.title = str(title)
        self.price = self.clean_price(price)
        self.rating = self.numeric_rating(rating)
        self.availability = self.clean_availability(availability)
        self.upc = upc
        self.description = (str(description)[:50]).replace("\n", " ") + "..."
        self.url = url

    @staticmethod
    def clean_price(price):
        match = re.search(r"[\d,.]+", price)
        if match:
            raw_price = match.group()
            cleaned_price = raw_price.replace(",", "")
            try:
                return float(cleaned_price)
            except ValueError:
                return 0.0
        return 0.0

    @staticmethod
    def clean_availability(availability):
        return int(re.search(r'\d+', availability).group())

    @staticmethod
    def numeric_rating(rating):

        score = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,}
        return score.get(rating.lower(), 0)

    def __repr__(self):
        return (f"Book: {self.title},\n"
                f"Price: {self.price}£,\n"
                f"Description: {self.description}...\n"
                f"Rating: {self.rating},\n"
                f"Availability: {self.availability},\n"
                f"UPC: {self.upc},\n"
                f"URL: {self.url}\n")

    def to_list(self) -> list:
        return [self.title,
                self.price,
                self.description,
                self.rating,
                self.availability,
                self.upc,
                self.url]
