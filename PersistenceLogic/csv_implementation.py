import csv
from os import path

from config.config import BOOKS_FILENAME, CSV_HEADER


def generate_csv():
    if not path.exists(BOOKS_FILENAME):
        with open(BOOKS_FILENAME, 'w', newline='', encoding="UTF-8-sig") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',)
            writer.writerow(CSV_HEADER)


def to_csv(book: list) -> None:
    with open(BOOKS_FILENAME, 'a', newline='', encoding="UTF-8-sig") as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(book)