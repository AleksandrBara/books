import requests
import os
from pathlib import Path
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filename


def donload_book_txt(book_id, file_name, folder):
    library_url = 'https://tululu.org/txt.php?id={}'.format(book_id)
    os.makedirs(folder, exist_ok=True)
    response = requests.get(library_url)
    response.raise_for_status()
    check_for_redirect(response)
    sanitized_filename = sanitize_filename('{}_{}'.format(
        file_name,
        book_id
    ))
    # print(sanitized_filename)
    file_extension = '.txt'
    book_path = os.path.join(folder, '{}{}'.format(sanitized_filename, file_extension))
    with open(book_path, 'w') as file:
        file.write(response.text)
    return book_path


def check_for_redirect(response):
    if response.history:
        raise requests.HTTPError


def get_book_info(book_id):
    url = 'https://tululu.org/b{}/'.format(book_id)
    response = requests.get(url)
    response.raise_for_status()
    check_for_redirect(response)
    soup = BeautifulSoup(response.text, 'lxml')
    book_jaket_tag = soup.find('body').find('h1')
    book_jaket_text = book_jaket_tag.text.split('::')
    book_name = book_jaket_text[0].strip()
    author = book_jaket_text[1].strip()
    return book_name, author


if __name__ == '__main__':
    start_book_id = 1
    end_book_id = 10
    folder = 'books'
    for book_id in range(start_book_id, end_book_id+1):
        try:
            file_name, aaa = get_book_info(book_id)
            donload_book_txt(book_id, file_name, folder)
        except (requests.ConnectionError) as e:
            print('Ошибка подключения: {} '.format(e))
        except (requests.HTTPError) as e:
            print('Книга с id = {}, не найдена '.format(book_id))
            continue






