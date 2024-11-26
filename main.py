from typing import Optional

from library import LibraryManager

# текст справки
MENU_INFO = """
Вам доступны следующие команды:
1. Добавить книгу; параметры (название книги, автор, год издания)
2. Удалить книгу; параметры (идентификатор книги)
3. Поиск книг; параметры (название книги, автор, год издания)
4. Отображение всех книг
5. Изменение статуса книги; параметры (идентификатор книги, статус)
6. Загрузка книг из файла с сохранением; параметры (путь к файлу сохранения)
7. Сохранение книг в json файл; параметры (путь к файлу сохранения)
8. Меню
9. Выход
Команды вводятся в формате: "<номер команды> <значение параметра 1>;<значение параметра 2>;..."
Например: команда добавления книги - введите: "1 Книга 6;Иванов И. И.;2024"
Пробелы после номера команды не учитываются
Если вам нужен пример текста команды введите слово "помощь" в запросе 
"""

# примеры корректных команд
EXAMPLES = {
    "1": "1 Книга 1;Иванов И. И.;2024",
    "2": "2 0",
    "3": "3 ;Иванов;",
    "4": "4",
    "5": "5 0;выдана",
    "6": "6 C:/Users/User/Documents/book_dump_26112024.json",
    "7": "7 C:/Users/User/Documents/book_dump_26112024.json",
    "8": "8",
    "9": "9"
}
# разделить параметров в запросе пользователя, например "книга 1;2024" => ("книга 1", "2024")
QUERY_PARAM_DELIMITER = ';'


#               блок с функциями обработки команд
def command_add_book(library_manager: LibraryManager, params: tuple):
    return library_manager.add_book(*params[:3])


def command_delete_book(library_manager: LibraryManager, params: tuple):
    return library_manager.delete_book(*params[:1])


def command_search_books(library_manager: LibraryManager, params: tuple):
    return library_manager.search_books(*params[:3])


def command_get_all_books(library_manager: LibraryManager, *args):
    return library_manager.get_all_books_info()


def command_change_status(library_manager: LibraryManager, params: tuple):
    return library_manager.change_book_status(*params[:2])


def command_load_books(library_manager: LibraryManager, params: tuple):
    return library_manager.load_books(*params[:1])


def command_save_books(library_manager: LibraryManager, params: tuple):
    return library_manager.dump_books(*params[:1])


# все основные команды системы управления библиотекой
ACTION_COMMANDS = {
    "1": command_add_book,
    "2": command_delete_book,
    "3": command_search_books,
    "4": command_get_all_books,
    "5": command_change_status,
    "6": command_load_books,
    "7": command_save_books
}


def main():
    save_path = input("Укажите путь к файлу сохранения если он есть иначе введите любой символ")
    # обработчик основных действия по взаимодействию с книгами и хранение книг в ram
    manager = LibraryManager()
    load_result = manager.load_books(save_path)
    if load_result:
        print(load_result)
    else:
        print('Сохранение загружено')

    print(MENU_INFO)
    while True:
        query = input()

        if not query:
            print("Введите команду")
            continue

        command_symbol = query[0]
        # сначала проверяем не указан ли параметр получения подсказки, тогда только выводим ее без активных действий
        if command_symbol.isdigit() and "помощь" in query:
            print(EXAMPLES.get(command_symbol, "такой команды не существует"))
            continue
        # выполнение команд действий (сбор параметров и отправка в соответсвующий обработчик)
        elif command_symbol in ACTION_COMMANDS:
            params = query[1:].strip().split(QUERY_PARAM_DELIMITER)
            # если было произведено действие из ACTION_COMMANDS - выводим результат действия или текст ошибки
            action_result: Optional[str] = ACTION_COMMANDS[command_symbol](manager, params)
            if action_result:
                print(action_result)
            else:
                print("Действие выполнено!")
        # вспомогательные команды, не связанные с управлением библиотеки
        elif command_symbol == "8":
            print(MENU_INFO)
            continue
        elif command_symbol == "9":
            break
        else:
            print(f"Введите корректную команду, команда ({command_symbol}) не предусмотрена")
            continue


if __name__ == '__main__':
    main()
