import unittest
from unittest.mock import patch
import io
from main import main
"""
команды:
1. Добавить книгу; параметры (название книги, автор, год издания)
2. Удалить книгу; параметры (идентификатор книги)
3. Поиск книг; параметры (название книги, автор, год издания)
4. Отображение всех книг
5. Изменение статуса книги; параметры (идентификатор книги, статус)
6. Загрузка книг из файла с сохранением; параметры (путь к файлу сохранения)
7. Сохранение книг в json файл; параметры (путь к файлу сохранения)
8. Меню
9. Выход
"""


# несколько небольших тестов
class TestLibraryApp(unittest.TestCase):
    # добавление книги и проверка добавления
    @patch('builtins.input', side_effect=[' ', '1 Книга 1;Иванов И. И.;2024', '4', '9'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_add(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Действие выполнено!', output)
        self.assertIn('ID: 0, название: Книга 1, автор: Иванов И. И., год издания: 2024, статус: в наличии', output)

    # проверка редактирования статуса
    @patch('builtins.input', side_effect=[' ', '1 Книга 1;Иванов И. И.;2024', '4', '5 0;выдана', '4', '9'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_change_status(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Действие выполнено!', output)
        self.assertIn('ID: 0, название: Книга 1, автор: Иванов И. И., год издания: 2024, статус: в наличии', output)
        self.assertIn('ID: 0, название: Книга 1, автор: Иванов И. И., год издания: 2024, статус: выдана', output)

    # проверка справки
    @patch('builtins.input', side_effect=[' ', '1 помощь', '9'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_support(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertNotIn('Действие выполнено!', output)
        self.assertIn('1 Книга 1;Иванов И. И.;2024', output)

    # проверка удаления
    @patch('builtins.input', side_effect=[' ', '1 Книга 1;Иванов И. И.;2024', '4', '2 0', '4', '9'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_delete(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Действие выполнено!', output)
        self.assertIn('ID: 0, название: Книга 1, автор: Иванов И. И., год издания: 2024, статус: в наличии', output)
        self.assertIn('Пока ни одной книги не добавлено в библиотеку', output)

    # проверка многократного удаления
    @patch('builtins.input', side_effect=[' ', '1 Книга 1;Иванов И. И.;2024', '4', '2 0', '2 0', '9'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_multiple_delete(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Действие выполнено!', output)
        self.assertIn('Книги с идентификатором: (0) не существует', output)

    # проверка сохранения (создать книгу - сохранить - удалить - восстановить из сохранения) => книга будет отображена
    @patch('builtins.input', side_effect=[' ', '1 Книга 1;Иванов И. И.;2024', '7 data/test_save.json', '2 0', '6 data/test_save.json', '4', '9'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_save_books(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn('ID: 0, название: Книга 1, автор: Иванов И. И., год издания: 2024, статус: в наличии', output)

    # проверка поиска
    @patch('builtins.input', side_effect=[' ', '1 Книга 1;Иванов И. И.;2023', '1 Книга 2;Иванов И. И.;2024', '3 ;;2023', '9'])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_save_books(self, mock_stdout, mock_input):
        main()
        output = mock_stdout.getvalue()
        self.assertIn('Найдено (1) книг:', output)
        self.assertIn('ID: 0, название: Книга 1, автор: Иванов И. И., год издания: 2023, статус: в наличии', output)


if __name__ == '__main__':
    unittest.main()
