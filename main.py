import requests
import os
from pathlib import Path


def donload_book(book_id):
    library_url = 'https://tululu.org/txt.php?id={}'.format(book_id)
    directory_name = 'books'
    os.makedirs(directory_name, exist_ok=True)
    response = requests.get(library_url)
    response.raise_for_status()
    file_name = 'id{}.txt'.format(book_id)
    file_path = Path(directory_name, file_name)
    with open(file_path, 'w') as file:
        file.write(response.text)

if __name__ == '__main__':
    book_id = 1
    while book_id <= 10:
        donload_book(book_id)
        book_id += 1




