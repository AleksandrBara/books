# Электронныя библиотека.

В репо представлен скрипт с помощью которого вы можете скачивать книги с сайта [tululu.org](tululu.orghttps://tululu.org/).

### Как работает:

- Скрипт автоматически создает папки:
  ```books``` и будет складывать туда скаченные книги и
  ```images```  туда попадут скаченные обложки.


### Установка.

- Скачайте код
- Python3 должен быть уже установлен.
  Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:

```bash
pip install -r requirements.txt
```

#### Запуск кода.

Для запуска кода:

```bash
python3 main.py --start_id=s_id --end_id=e_id
``` 

, где `s_id` - это номер первой книги с которого начнется скачивание, а `e_id` номер последней.



## Цели проекта

Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).