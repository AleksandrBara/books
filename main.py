import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename
from urllib.parse import urljoin, urlparse, urlsplit

BASE_URL ='https://tululu.org'


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
    book_path = os.path.join(folder, '{}{}'.format(sanitized_filename, file_extension))
    with open(book_path, 'w') as file:
        file.write(response.text)
    return book_path


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_info(book_id):
    url = '{}/b{}/'.format(BASE_URL, book_id)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    book_name_tag = soup.find('body').find('h1')
    book_name_text = book_name_tag.text.split('::')
    book_name = book_name_text[0].strip()
    book_author = book_name_text[1].strip()
    book_jaket_tag = soup.find(class_='bookimage').find('img')['src']
    book_jaket_url = urljoin(BASE_URL, book_jaket_tag)
    return book_name, book_author, book_jaket_url


def download_book_jacket(url, folder):
    os.makedirs(folder, exist_ok=True)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    file_name = os.path.basename(urlsplit(url).path)
    sanitized_filename = sanitize_filename(file_name)
    book_jacket_path = os.path.join(folder, sanitized_filename)
    with open(book_jacket_path, 'wb') as out_file:
        out_file.write(response.content)


if __name__ == '__main__':
    start_book_id = 1
    end_book_id = 10
    folder = 'books'
    img_folder = 'images'
    for book_id in range(start_book_id, end_book_id+1):
        try:
            book_name, book_author, book_jacket_url = get_book_info(book_id)
            donload_book_txt(book_id, book_name, folder)
            download_book_jacket(book_jacket_url, img_folder)
        except (requests.ConnectionError) as e:
            print('Ошибка подключения: {} '.format(e))
        except (requests.HTTPError) as e:
            print('Книга с id = {}, не найдена '.format(book_id))
            continue






