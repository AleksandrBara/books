# Электронная библиотека.

**Скрипты с помощью которых вы можете скачивать книги с сайта** [tululu.org](https://tululu.org/).

### Как это работает:

**В репо представлены 2 скрипта, с помощью которых вы можете скачивать любое количество книг,
единственное ограничение - это количество книг на сайте**.

- `books_parser.py` - Использует для скачивания идентификатор (`id`), книги. 
По умолчанию. качает книги с 1 по 10. Задать диапазон можно командами `start_id` и `end_id`

- `parse_tululu_category.py` - Скачивает подборkу книг и имеет большое количество настроек, 
а так же создает файл `books.json` с полной информацией о книгах. 
По умолчанию скачивает книги категории (`books_category=55`) "Научная фантастика". 
Обладает высокой функциональностью и включат в себя следующие настройки:

  - `start_page` - Номер страницы с которого начнется скачивание, по умолчантю 1
  - `end_page` - Номер страницы до которой будут скачиваться книги, по умолчанию 1
  - `books_category` - Подборка книг, по умолчанию 55 (Фантастика)
  - `skip_img` - Отменяет скачивание обложек, по умолчанию `False`
  - `skip_txt` - Отменяет скачивание книг, по умолчанию `False`
  - `dest_folder` - Дериктория куда будет сохранены скаченные файлы, по умолчанию базовая.
  - `json_path` - Путь к файлу .json в котором находится информация о скаченных книгах, по умолчанию `books.json`



### Установка.

- Скачайте код
- Python3 должен быть уже установлен.
  Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:

```bash
pip install -r requirements.txt
```

### Запуск кода.

#### Пример запуска `books_parser.py`:

```bash
python3 books_parser.py --start_id=5 --end_id=7
``` 

Код скачает три книги с `id` = 5,6,7

Если запустить файл без параметров - скачаются книги с `id` 1 - 10. 

#### Пример запуска  `parse_tululu_category.py`:

```bash
python3 parse_tululu_category.py --start_page=1 --end_page=10 --books_category=62 --skip_img=True

``` 
Код скачает в домашнюю директорию книги без обложек с 1 по 10 страницы категории `62` Поэзия.


## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
