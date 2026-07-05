import pytest
from main import BooksCollector


class TestBooksCollector:
    # Фикстура: создает новый экземпляр коллектора перед каждым тестом.
    @pytest.fixture
    def collector(self):
        return BooksCollector()

    # 1. Проверка успешного добавления книги (позитивный сценарий)
    def test_add_new_book_success(self, collector):
        collector.add_new_book("Гарри Поттер")
        books_genre = collector.get_books_genre()
        assert "Гарри Поттер" in books_genre
        # Подсказка из задания: у добавленной книги нет жанра (пустая строка)
        assert books_genre["Гарри Поттер"] == ''

    # 2. Проверка ограничений на длину названия и уникальность (негативный + дубликаты)
    @pytest.mark.parametrize("book_name", [
        "",                 # Пустое имя
        "A" * 41,           # Имя длиннее 40 символов
    ])
    def test_add_new_book_invalid_length_or_empty(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

    def test_add_duplicate_book_is_ignored(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 1")  # Повторная попытка
        books = list(collector.get_books_genre().keys())
        assert books.count("Книга 1") == 1

    # 3. Установка жанра существующей книге (позитивный) и отказ при ошибках (негативный)
    def test_set_book_genre_success(self, collector):
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_book_genre("Оно") == "Ужасы"

    @pytest.mark.parametrize("name, genre", [
        ("Несуществующая книга", "Фантастика"),  # Книги нет в словаре
        ("Властелин Колец", "Космос"),           # Жанра нет в списке доступных
    ])
    def test_set_book_genre_failure(self, collector, name, genre):
        if name != "Несуществующая книга":
            collector.add_new_book(name) 
        
        state_before = collector.get_book_genre(name)
        collector.set_book_genre(name, genre)
        # Состояние не должно измениться
        assert collector.get_book_genre(name) == state_before

    # 4. Получение жанра по имени
    def test_get_book_genre_returns_none_for_unset(self, collector):
        collector.add_new_book("Пустой жанр")
        assert collector.get_book_genre("Пустой жанр") is None

    # 5. Вывод списка книг с определённым жанром
    def test_get_books_with_specific_genre(self, collector):
        collector.add_new_book("Шерлок Холмс")
        collector.set_book_genre("Шерлок Холмс", "Детективы")
        collector.add_new_book("Иван Васильевич")
        collector.set_book_genre("Иван Васильевич", "Комедии")
        
        result = collector.get_books_with_specific_genre("Детективы")
        # Порядок в списках может отличаться, поэтому сравниваем отсортированные массивы
        assert sorted(result) == ["Шерлок Холмс"]

    # 6. Получение всего словаря книг
    def test_get_books_genre_returns_current_state(self, collector):
        collector.add_new_book("Метро 2033")
        full_dict = collector.get_books_genre()
        assert isinstance(full_dict, dict)
        assert "Метро 2033" in full_dict

    # 7. Книги с возрастным рейтингом отсутствуют в списке для детей
    def test_get_books_for_children_excludes_age_rating(self, collector):
        collector.add_new_book("Трое из Простоквашино")
        collector.add_new_book("Сияние")
        collector.set_book_genre("Трое из Простоквашино", "Мультфильмы")
        collector.set_book_genre("Сияние", "Ужасы")  # Есть в genre_age_rating
        
        children_books = collector.get_books_for_children()
        assert "Трое из Простоквашино" in children_books
        assert "Сияние" not in children_books

    # 8. Добавление в избранное существующих книг без дублей
    def test_favorites_flow_and_duplicates_protection(self, collector):
        collector.add_new_book("Дюна")
        collector.set_book_genre("Дюна", "Фантастика")
        
        collector.add_book_in_favorites("Дюна")
        assert collector.get_list_of_favorites_books() == ["Дюна"]
        
        # Попытка добавить дубль
        collector.add_book_in_favorites("Дюна")
        favorites = collector.get_list_of_favorites_books()
        assert favorites.count("Дюна") == 1

        # Попытка добавить книгу, которой нет в библиотеке
        collector.add_book_in_favorites("Неведомая книга")
        assert "Неведомая книга" not in collector.get_list_of_favorites_books()

    # Дополнительные тесты для блока избранного
    def test_cannot_add_book_to_favorites_without_genre(self, collector):
        """Проверяем бизнес-логику: нельзя добавить в избранное книгу без назначенного жанра."""
        collector.add_new_book("Безжанровая книга")
        collector.add_book_in_favorites("Безжанровая книга")
        assert "Безжанровая книга" not in collector.get_list_of_favorites_books()

    # 9. Удаление из избранного существующего и отсутствующего элемента
    def test_delete_from_favorites(self, collector):
        collector.add_new_book("Нейромант")
        collector.set_book_genre("Нейромант", "Фантастика")
        collector.add_book_in_favorites("Нейромант")
        
        collector.delete_book_from_favorites("Нейромант")
        assert "Нейромант" not in collector.get_list_of_favorites_books()
        
        # Негативная проверка: удаление того, чего нет (не ломает список)
        prev_count = len(collector.get_list_of_favorites_books())
        collector.delete_book_from_favorites("Нейромант")
        assert len(collector.get_list_of_favorites_books()) == prev_count

    def test_delete_nonexistent_from_favorites_on_empty_list(self, collector):
        """Удаление из пустого избранного не должно вызывать ошибок."""
        collector.delete_book_from_favorites("Кто угодно")
        assert collector.get_list_of_favorites_books() == []
