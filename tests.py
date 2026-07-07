import pytest
from main import BooksCollector

class TestBooksCollector:
    @pytest.fixture
    def collector(self):
        """Создает чистый экземпляр коллектора и список допустимых жанров."""
        c = BooksCollector()
        # Инициализируем словарь доступных жанров, чтобы тесты set_book_genre работали корректно.
        # Если у класса нет такого публичного метода, создайте его в main.py 
        # или инициализируйте этот атрибут напрямую в __init__.
        if hasattr(c, 'set_available_genres'):
            c.set_available_genres([
                "Фантастика", "Детективы", "Комедии", "Ужасы", 
                "Мультфильмы", "Космос"
            ])
        return c

    # 1. Проверка успешного добавления книги (позитивный сценарий)
    def test_add_new_book_success(self, collector):
        collector.add_new_book("Гарри Поттер")
        books_genre = collector.get_books_genre()
        assert "Гарри Поттер" in books_genre
        assert books_genre["Гарри Поттер"] == ''

    # 2. Позитивная проверка границ длины имени (исправление линии 21-22)
    def test_add_new_book_boundary_lengths(self, collector):
        name_min = "A"
        name_max = "B" * 40
        
        collector.add_new_book(name_min)
        collector.add_new_book(name_max)
        
import pytest
from main import BooksCollector

class TestBooksCollector:
    @pytest.fixture
    def collector(self):
        """Создает чистый экземпляр коллектора перед каждым тестом."""
        c = BooksCollector()
        # Инициализация списка допустимых жанров для работы метода set_book_genre.
        # Если в вашем классе нет такого публичного метода, инициализируйте 
        # соответствующий атрибут напрямую или через конструктор __init__.
        if hasattr(c, 'set_available_genres'):
            c.set_available_genres([
                "Фантастика", "Детективы", "Комедии", "Ужасы", 
                "Мультфильмы", "Космос"
            ])
        return c

    # 1. Проверка успешного добавления книги (позитивный сценарий)
    def test_add_new_book_success(self, collector):
        collector.add_new_book("Гарри Поттер")
        books_genre = collector.get_books_genre()
        assert "Гарри Поттер" in books_genre
        assert books_genre["Гарри Поттер"] == ''

    # 2. Позитивная проверка граничных значений длины имени (исправление строк 21-22)
    @pytest.mark.parametrize("book_name", [
        "A",                # Минимальная длина: 1 символ
        "B" * 39,           # Длина строго меньше максимума
        "C" * 40,           # Максимальная длина: 40 символов
    ])
    def test_add_new_book_valid_lengths(self, collector, book_name):
        """Позитивный сценарий: книги с валидной длиной успешно добавляются."""
        collector.add_new_book(book_name)
        books = collector.get_books_genre()
        assert book_name in books
        assert books[book_name] == ''

    # 2. Негативная проверка длины и пустоты (только провальные сценарии)
    @pytest.mark.parametrize("book_name", [
        "",                 # Пустое имя
        "D" * 41,           # Имя длиннее 40 символов
    ])
    def test_add_new_book_invalid_length_or_empty(self, collector, book_name):
        collector.add_new_book(book_name)
        assert book_name not in collector.get_books_genre()

    def test_add_duplicate_book_is_ignored(self, collector):
        collector.add_new_book("Книга 1")
        collector.add_new_book("Книга 1")  # Повторная попытка
        books = list(collector.get_books_genre().keys())
        assert books.count("Книга 1") == 1

    # 3. Установка жанра существующей книге (позитивный) 
    def test_set_book_genre_success(self, collector):
        collector.add_new_book("Оно")
        collector.set_book_genre("Оно", "Ужасы")
        assert collector.get_book_genre("Оно") == "Ужасы"

    # 3. Отказ при ошибках (негативный). Убраны условия IF (исправление логики параметризации)
    def test_set_book_genre_fails_for_nonexistent_book(self, collector):
        name = "Несуществующая книга"
        state_before = collector.get_book_genre(name)
        collector.set_book_genre(name, "Фантастика")
        assert collector.get_book_genre(name) == state_before

    def test_set_book_genre_fails_for_invalid_genre(self, collector):
        valid_book = "Властелин Колец"
        invalid_genre = "Космос"
        
        collector.add_new_book(valid_book)
        state_before = collector.get_book_genre(valid_book)
        
        collector.set_book_genre(valid_book, invalid_genre)
        assert collector.get_book_genre(valid_book) == state_before

    # 4. Получение жанра по имени (для новой книги без установленного жанра)
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
        assert isinstance(result, list)
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
        collector.set_book_genre("Сияние", "Ужасы")  
        
        children_books = collector.get_books_for_children()
        assert isinstance(children_books, list)
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
        assert len(favorites) == 1
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

    # 9. Удаление из избранного существующего элемента
    def test_delete_from_favorites_existing_item(self, collector):
        collector.add_new_book("Нейромант")
        collector.set_book_genre("Нейромант", "Фантастика")
        collector.add_book_in_favorites("Нейромант")
        
        collector.delete_book_from_favorites("Нейромант")
        assert "Нейромант" not in collector.get_list_of_favorites_books()

    # 9. Удаление отсутствующего элемента из непустого избранного (не ломает список)
    def test_delete_nonexistent_from_favorites_on_populated_list(self, collector):
        collector.add_new_book("Князь Серебряный")
        collector.set_book_genre("Князь Серебряный", "История")
        collector.add_book_in_favorites("Князь Серебряный")
        
        prev_count = len(collector.get_list_of_favorites_books())
        collector.delete_book_from_favorites("Кто угодно")
        assert len(collector.get_list_of_favorites_books()) == prev_count

    # 9. Удаление из пустого избранного не должно вызывать ошибок
    def test_delete_nonexistent_from_favorites_on_empty_list(self, collector):
        initial_state = collector.get_list_of_favorites_books()
        collector.delete_book_from_favorites("Кто угодно")
        assert collector.get_list_of_favorites_books() == initial_state
