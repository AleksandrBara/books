import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit, urlparse
import argparse
from time import sleep
from main import (check_for_redirect, donload_book_txt,
                  download_book_jacket, parse_book_page
                  )
from pprint import pprint
import json
from requests import HTTPError, ConnectionError

BASE_URL = 'https://tululu.org'


def parse_books_urls(response):
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.find('div', id='content').find_all('table')
    one_page_books_urls = list()
    for book in books:
        book_id = book.find('a')['href']
        book_url = urljoin(response.url, book_id)
        one_page_books_urls.append(book_url)
    return one_page_books_urls


if __name__ == '__main__':
    books_category = 'l55'
    category_url = urljoin(BASE_URL,books_category)
    last_page = 1
    first_page = 1
    books_urls = list()
    for page_number in range(first_page, last_page + 1):
        new_page_url = urljoin(category_url, str(page_number))
        try:
            response = requests.get(new_page_url)
            response.raise_for_status()
            on_page_books_urls = parse_books_urls(response)
            books_urls.extend(on_page_books_urls)
        except (ConnectionError, HTTPError) as e:
            print('Ошибка подключения: {} '.format(e))
            sleep(600)

    txt_folder = 'books'
    img_folder = 'images'
    books_description = list()
    for book_url in books_urls:
        book_id = urlparse(book_url).path.replace('/', '').replace('b', '')
        book_txt_url = urljoin(BASE_URL, 'txt.php')
        try:
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            book = parse_book_page(book_response)
            book_path = donload_book_txt(
                book_txt_url,
                book_id,
                book['book_name'],
                txt_folder
            )
            book_jacket_path = download_book_jacket(book['book_jacket'], img_folder)
        except (requests.ConnectionError) as e:
            print('Ошибка подключения: {} '.format(e))
            sleep(600)
        except (requests.HTTPError) as e:
            print('Книга с id = {}, не найдена '.format(book_id))
            continue
        book_description = {
            'title': book['book_name'],
            'author': book['author'],
            'img_src': book_jacket_path,
            'book_path': book_path,
            'comments': book['comments'],
            'genre': book['genre']}
        books_description.append(book_description)
    json_file_extension, json_file_name = ".json", "books_deskription"
    json_file_path = os.path.join('{}{}'.format(
        json_file_name,
        json_file_extension
    ))
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(
            books_description,
            file,
            ensure_ascii=False,
            indent=4,
            sort_keys=False
        )
