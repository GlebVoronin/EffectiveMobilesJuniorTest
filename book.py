# импорт встроенных библиотек для аннотирования и упрощения кода
from typing import Optional
from dataclasses import dataclass, field, asdict


@dataclass
class Book:
    """Класс для хранения данных и состояния по каждой книге"""
    id: int
    title: str
    author: str
    year: int
    status: str = field(default="в наличии")

    def change_status(self, status: str) -> Optional[str]:
        """
        Метод меняет статус книги на указанный пользователем [status],
        производится проверка на допустимость использования введенного статуса.
        :return None при успешной смене статуса, строка ошибки в случае ввода некорректного статуса
        """
        valid_statuses = {"в наличии", "выдана"}
        if status in valid_statuses:
            self.status = status
        else:
            return f"Статус {status} не предусмотрен"

    def to_dict(self) -> dict:
        """Метод получения сведений книги в виде словаря (вспомогательный)"""
        return asdict(self)

    def get_info(self) -> str:
        """Метод получения сведений книги в виде строки для вывода человеку"""
        book_info = self.to_dict()
        translate_param_names = {
            "id": "ID",
            "title": "название",
            "author": "автор",
            "year": "год издания",
            "status": "статус"
        }
        return ', '.join([f"{translate_param_names[param]}: {value}" for param, value in book_info.items()])
