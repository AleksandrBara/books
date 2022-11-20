import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlsplit, urlparse
import argparse
from time import sleep
from books_parser import (check_for_redirect, donload_book_txt,
                          download_book_jacket, parse_book_page
                          )
import json
from requests import HTTPError, ConnectionError

BASE_URL = 'https://tululu.org'
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def parse_books_urls(response):
    soup = BeautifulSoup(response.text, 'lxml')
    books = soup.find('div', id='content').find_all('table')
    one_page_books_urls = list()
    for book in books:
        book_id = book.find('a')['href']
        book_url = urljoin(response.url, book_id)
        one_page_books_urls.append(book_url)
    return one_page_books_urls


def get_args(base_dir, json_file_name='books.json'):
    parser = argparse.ArgumentParser(
        description='Скрипт для скачивания электронных книг'
    )
    parser.add_argument('--start_page', type=int, default=1,
                        help='Номер стартовой страницы в категории'
                        )
    parser.add_argument('--end_page', type=int, default=1,
                        help='Номер последней страницы в категории'
                        )
    parser.add_argument('--books_category', type=int, default=55,
                        help='Категория подборки книг'
                        )
    parser.add_argument('--skip_img', action='store_true',
                        help='Параметр позволяет не скачивать обложки(True)'
                        )
    parser.add_argument('--skip_txt', action='store_true',
                        help='Параметр позволяет не скачивать txt файл(True)'
                        )
    parser.add_argument('--dest_folder', type=str, default=base_dir,
                        help='Задать папку для скачивания'
                        )
    parser.add_argument('--json_path', type=str,
                        default=os.path.join(base_dir, json_file_name),
                        help='Путь к файлу .json'
                        )
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args(BASE_DIR)
    books_category = args.books_category
    last_page = args.end_page
    first_page = args.start_page
    skip_txt = args.skip_txt
    skip_img = args.skip_img
    dest_folder = args.dest_folder
    json_file_path = args.json_path

    books_urls = list()
    for page_number in range(first_page, last_page + 1):
        new_page_url = urljoin(BASE_URL, '/l{}/{}'.format(
            books_category,
            page_number
        ))
        try:
            response = requests.get(new_page_url)
            response.raise_for_status()
            check_for_redirect(response)
            on_page_books_urls = parse_books_urls(response)
            books_urls.extend(on_page_books_urls)
        except ConnectionError as e:
            print('Ошибка подключения: {} '.format(e))
            sleep(600)
        except HTTPError as e:
            print('Страницы {} в ктегории {} не существует'.format(
                page_number,
                books_category
            ))
            print('Ошибка: {} '.format(e))
            break

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
            if not skip_txt:
                book_path = donload_book_txt(
                    book_txt_url,
                    book_id,
                    book['book_name'],
                    txt_folder
                )
            if not skip_img:
                book_jacket_path = download_book_jacket(book['book_jacket'], img_folder)
        except ConnectionError as e:
            print('Ошибка подключения: {} '.format(e))
            sleep(600)
        except HTTPError as e:
            print('Книга с id = {}, не доступна для скачивания'.format(book_id))
            continue
        book_description = {
            'title': book['book_name'],
            'author': book['author'],
            'img_src': book_jacket_path,
            'book_path': book_path,
            'comments': book['comments'],
            'genres': book['genres']}
        books_description.append(book_description)
    with open(json_file_path, 'w', encoding='utf-8') as file:
        json.dump(
            books_description,
            file,
            ensure_ascii=False,
            indent=4,
            sort_keys=False
        )
