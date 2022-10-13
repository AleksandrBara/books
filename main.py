import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlsplit
import argparse


BASE_URL = 'https://tululu.org'


def donload_book_txt(book_id, file_name, folder):
    library_url = '{}/txt.php?id={}'.format(BASE_URL, book_id)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(library_url)
    response.raise_for_status()
    check_for_redirect(response)
    sanitized_filename = sanitize_filename('{}_{}'.format(
        file_name,
        book_id
    ))
    file_extension = '.txt'
    book_path = Path(folder, '{}{}'.format(sanitized_filename, file_extension))
    with open(book_path, 'w') as file:
        file.write(response.text)


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def parse_book_page(response):
    soup = BeautifulSoup(response.text, 'lxml')
    book_name_tag = soup.find('body').find('h1')
    book_name_text = book_name_tag.text.split('::')
    book_name = book_name_text[0].strip()
    book_author = book_name_text[1].strip()
    book_jaket_tag = soup.find(class_='bookimage').find('img')['src']
    book_jaket_url = urljoin(BASE_URL, book_jaket_tag)
    comments_tag = soup.find('div', id='content').find_all('span', class_='black')
    comments = [comment.text for comment in comments_tag]
    book_genre_tag = soup.find('span', class_='d_book').find('a')['title']
    book_genre = book_genre_tag.split('-')[0]
    return {
        'book_name': book_name,
        'author': book_author,
        'book_jacket': book_jaket_url,
        'comments': comments,
        'genre': book_genre
    }


def download_book_jacket(url, folder):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = os.path.basename(urlsplit(url).path)
    sanitized_filename = sanitize_filename(file_name)
    book_jacket_path = Path(folder, sanitized_filename)
    with open(book_jacket_path, 'wb') as file:
        file.write(response.content)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('start_id', type=int, default=1)
    parser.add_argument('end_id', type=int, default=10)
    return parser.parse_args()


if __name__ == '__main__':
    args = get_args()
    book_start_id = args.start_id
    book_end_id = args.end_id
    txt_folder = 'books'
    img_folder = 'images'
    for book_id in range(book_start_id, book_end_id + 1):
        book_url = '{}/b{}/'.format(BASE_URL, book_id)
        try:
            book_response = requests.get(book_url)
            book_response.raise_for_status()
            check_for_redirect(book_response)
            book_info = parse_book_page(book_response)
            donload_book_txt(book_id, book_info['book_name'], txt_folder)
            download_book_jacket(book_info['book_jacket'], img_folder)
        except (requests.ConnectionError) as e:
            print('Ошибка подключения: {} '.format(e))
        except (requests.HTTPError) as e:
            print('Книга с id = {}, не найдена '.format(book_id))
            continue
