# импорт встроенных библиотек для аннотирования и упрощения кода
import json
import os
import re
from typing import Union, Dict, Optional
from dataclasses import dataclass, field

from book import Book


@dataclass
class LibraryManager:
    books: Dict[int, Book] = field(default_factory=dict)

    def load_books(self, save_path: str) -> Optional[str]:
        """
        Загрузка книг из сохранения (json файл)
        :param save_path: путь к json файлу с сохраненными данными книг
        :return: None при успешной загрузке книг, строка ошибки в случае проблем чтения
        """
        # проверка существования файла по указанному пути
        if not os.path.isfile(save_path):
            return f"Файл не обнаружен ({save_path}), будет выполнена инициализация пустой библиотеки"
        try:
            # загрузка книг
            with open(save_path, "r", encoding="utf-8") as file:
                books_data: Dict[int, Dict[str, Union[str, int]]] = json.load(file)
            # сбрасываем текущие сохраненные книги и вносим только книги из сохранения
            self.books.clear()
            for book_id, book_data in books_data.items():
                self.books[int(book_id)] = Book(**book_data)
        # проверка корректности чтения json-файла
        except json.JSONDecodeError:
            return "Ошибка чтения json файла, будет выполнена инициализация пустой библиотеки"

    def dump_books(self, save_path: str) -> Optional[str]:
        """
        Выгрузка книг в json файл
        :param save_path: путь к json файлу с сохраненными данными книг
        :return: None при успешном сохранении книг, строка ошибки в случае проблем выгрузки
        """
        # создаем директорию на случай отсутствия такой у пользователя
        save_directory, _ = os.path.split(save_path)
        os.makedirs(save_directory, exist_ok=True)
        try:
            with open(save_path, "w", encoding="utf-8") as file:
                json.dump({_id: book.to_dict() for _id, book in self.books.items()}, file, ensure_ascii=False, indent=4)
        # обработка ошибок, например, связанных с отсутствием разрешений на запись в указанной директории
        except Exception as err:
            return f"Непредвиденная ошибка: {err}"

    @staticmethod
    def validate_int_field(param_value: str) -> bool:
        """Метод проверки значения на возможность преобразовать в число"""
        # регулярное выражение, т.к. str.isdigit вернет True не только для цифр, которые можно сразу преобразовать в int
        return bool(re.match('[0-9]', param_value))

    def add_book(self, title: str = None, author: str = None, year: str = None) -> Optional[str]:
        """
        Метод добавляет книгу с введенными пользователем названием [title], автором [author], годом издания [year]
        :return: None при успешном добавлении книги, строка ошибки в обратном случае
        """
        # проверяется какой параметр был незаполнен и пользователю сообщается что нужно было заполнить
        param_data = {'название': title, 'автор': author, 'год издания': year}
        if not all(param_data.values()):
            missed = [param for param, value in param_data.items() if not value]
            return f"Ошибка: заполнены не все данные, заполните: ({', '.join(missed)})"
        # проверка корректности указания года, например, он не может быть буквой
        if not self.validate_int_field(year):
            return "Год издания указан некорректно, должен содержать только цифры"

        # идентификатор реализован как автоинкремент, начиная с 0
        book_id = max(self.books, default=-1) + 1

        self.books[book_id] = Book(book_id, title, author, int(year))

    def change_book_status(self, identifier: str = None, status: str = None) -> Optional[str]:
        """
        Метод меняет статус книги c идентификатором [identifier] на статус [status]
        :return None при успешной смене статуса, строка ошибки в случае некорректности статуса или отсутствия книги
        """
        # проверка наличия необходимых данных, вывод пользователю недостающих полей
        param_data = {'идентификатор': identifier, 'статус': status}
        if not all(param_data.values()):
            missed = [param for param, value in param_data.items() if not value]
            return f"Ошибка: заполнены не все данные, заполните: ({', '.join(missed)})"

        if not self.validate_int_field(identifier):
            return "Идентификатор книги указан некорректно, должен содержать только цифры"

        identifier = int(identifier)

        if identifier not in self.books:
            return f"Книги с идентификатором: ({identifier}) не существует"
        return self.books[identifier].change_status(status)

    def search_books(self, title: str = None, author: str = None, year: str = None) -> str:
        """
        Метод поиска книг, возвращает строку с результатами поиска или строк об ошибке
        Поиск производится по всем непустым параметрам из запроса пользователя,
        строки проверяются по вхождению в данные книги, год издания - по совпадению
        """

        # проверка входных данных на заполненность и корректность формата ввода
        if not any([title, author, year]):
            return "Ошибка: вы не ввели ни одного параметра для поиска"
        # если год указан - он должен быть валидным
        if year and not self.validate_int_field(year):
            return "Год издания указан некорректно, должен содержать только цифры"
        elif year:
            year = int(year)

        # сбор подходящих по критериям отбора объектов книг
        result: list[Book] = []
        for book in self.books.values():
            if title and title not in book.title:
                continue
            if author and author not in book.author:
                continue
            if year and year != book.year:
                continue
            result.append(book)

        if not result:
            return f"Ни одной книги по заданным параметрам (название;автор;год)=({title}; {author}; {year}) не найдено"
        return f"Найдено ({len(result)}) книг:\n" + "\n".join(book.get_info() for book in result)

    def delete_book(self, identifier: str) -> Optional[str]:
        """Метод удаления книги по ее идентификатору [identifier]"""

        if not self.validate_int_field(identifier):
            return "Идентификатор книги указан некорректно, должен содержать только цифры"

        identifier = int(identifier)

        if identifier not in self.books:
            return f"Книги с идентификатором: ({identifier}) не существует"

        del self.books[identifier]

    def get_all_books_info(self):
        """Метод получения сведений о всех книгах, возвращает одной строкой все данные о книгах"""
        if not self.books:
            return "Пока ни одной книги не добавлено в библиотеку"

        return "\n".join(book.get_info() for book in self.books.values())
