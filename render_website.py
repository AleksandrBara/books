import json
from livereload import Server, shell
from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
from pprint import pprint
from more_itertools import chunked

def on_reload():
    with open("books.json") as file:
        books = json.load(file)
    hulf_of_books = len(books) // 2
    chuncked_books = list(chunked(books, hulf_of_books))
    template = env.get_template('template.html')
    rendered_page = template.render(chuncked_books=chuncked_books)
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    print("page reloaded!")


if __name__ == '__main__':
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    server = Server()
    server.watch('template.html',on_reload())
    server.serve(root='.')