import json
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape
from more_itertools import chunked
import os
from math import ceil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


def on_reload():
    with open("books.json") as file:
        books = json.load(file)
    html_pages_path = os.path.join(BASE_DIR, 'html_pages')
    os.makedirs(html_pages_path, exist_ok=True)
    number_of_books_per_page = 20
    rows_per_page = 10
    number_of_pages = ceil(len(books) / number_of_books_per_page)
    chuncked_books = list(chunked(books, number_of_books_per_page))
    last_page = len(chuncked_books) - 1
    for num, books in enumerate(chuncked_books):
        template = env.get_template('template.html')
        page_path = os.path.join(
            html_pages_path,
            'index{}.html'.format(num))
        chuncked_books = list(chunked(books, rows_per_page))
        rendered_page = template.render(
            chuncked_books=chuncked_books,
            number_of_pages=number_of_pages,
            current_page_number=num,
            last_page=last_page
        )
        with open(page_path, 'w', encoding="utf8") as file:
            file.write(rendered_page)
        print("page reloaded!")


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    on_reload()

    server = Server()

    server.watch('template.html', on_reload)

    server.serve(root='.')
