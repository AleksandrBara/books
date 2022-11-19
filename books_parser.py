import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
import argparse
from time import sleep

BASE_URL = 'https://tululu.org'


def donload_book_txt(book_txt_url, book_id, file_name, folder):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(
        urljoin(BASE_URL, book_txt_url),
        params={'id': book_id}
    )
    response.raise_for_status()
    check_for_redirect(response)
    sanitized_filename = sanitize_filename('{}_{}'.format(
        file_name,
        book_id
    ))
    file_extension = '.txt'
    book_path = os.path.join(folder, '{}{}'.format(sanitized_filename, file_extension))
    with open(book_path, 'w') as file:
        file.write(response.text)
    return book_path


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')

    page_title = soup.head.title.text.split(',')
    try:
        book_name, string_with_author = page_title[0].split(' - ')
        book_author = string_with_author.split(',')[0]
    except ValueError:
        page_title = soup.head.title.text.split(' - ')
        book_name = page_title[0]
        book_author = page_title[1].split(',')[0]

    book_jaket_select = 'body table .bookimage img'
    book_jaket_img = soup.select_one(book_jaket_select)['src']
    book_jaket_url = urljoin(response.url, book_jaket_img)

    comments_select = 'body div.texts span.black'
    comments = soup.select(comments_select)
    comments_text = [comment.text for comment in comments]

    book_genres_select = 'span.d_book a'
    genre_tags = soup.select(book_genres_select)
    book_genres = [tag.text for tag in genre_tags]

    return {
        'book_name': book_name,
        'author': book_author,
        'book_jacket': book_jaket_url,
        'comments': comments_text,
        'genre': book_genres
    }


def download_book_jacket(url, folder):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = os.path.basename(urlsplit(url).path)
    sanitized_filename = sanitize_filename(file_name)
    book_jacket_path = os.path.join(folder, sanitized_filename)
    with open(book_jacket_path, 'wb') as file:
        file.write(response.content)
    return book_jacket_path


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_id', type=int, default=1)
    parser.add_argument('--end_id', type=int, default=10)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    book_start_id = args.start_id
    book_end_id = args.end_id
    txt_folder = 'books'
    img_folder = 'images'
    for book_id in range(book_start_id, book_end_id + 1):
        book_url = '{}/b{}/'.format(BASE_URL, book_id)
        book_txt_url = urljoin(BASE_URL, 'txt.php')
        try:
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            book = parse_book_page(book_response)
            donload_book_txt(book_txt_url, book_id, book['book_name'], txt_folder)
            download_book_jacket(book['book_jacket'], img_folder)
        except (requests.ConnectionError) as e:
            print('Ошибка подключения: {} '.format(e))
            sleep(600)
        except (requests.HTTPError) as e:
            print('Книга с id = {}, не найдена '.format(book_id))
            continue
