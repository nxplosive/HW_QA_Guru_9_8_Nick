"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product_book():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture
def product_shlapa():
    return Product("shlapa", 1000000, "Mega shlapa 3000", 3)


@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product_book, product_shlapa):
        # TODO напишите проверки на метод check_quantity
        assert product_book.check_quantity(1000) == True
        assert product_book.check_quantity(1) == True
        assert product_book.check_quantity(10000) == False
        assert product_shlapa.check_quantity(2) == True
        assert product_shlapa.check_quantity(5) == False

    def test_product_buy(self, product_book, product_shlapa):
        # TODO напишите проверки на метод buy
        product_book.buy(10)
        assert product_book.quantity == 990
        product_shlapa.buy(1)
        assert product_shlapa.quantity == 2

    def test_product_buy_more_that_available(self, product_book, product_shlapa):
        # TODO напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product_shlapa.buy(5)
        with pytest.raises(ValueError):
            product_book.buy(1001)


class TestCart:
    """
    TODO Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """

    def test_add_product(self, cart, product_book, product_shlapa):
        cart.add_product(product_book, 5)
        assert cart.products.get(product_book) == 5
        cart.add_product(product_shlapa, 2)
        assert cart.products.get(product_shlapa) == 2

    def test_negative_add(self, cart, product_shlapa, product_book):
        with pytest.raises(ValueError):
            cart.add_product(product_shlapa, 0)
        with pytest.raises(ValueError):
            cart.add_product(product_book, 0)

    def test_remove_product(self, product_book, product_shlapa, cart):
        cart.add_product(product_book, 4)
        cart.remove_product(product_book, 1)
        assert cart.products.get(product_book) == 3
        cart.add_product(product_shlapa, 3)
        cart.remove_product(product_shlapa, 1)
        assert cart.products.get(product_shlapa) == 2

    def test_remove_all_products(self, product_book, product_shlapa, cart):
        cart.add_product(product_book, 4)
        cart.remove_product(product_book, 4)
        assert cart.products.get(product_book) == None
        cart.add_product(product_shlapa, 2)
        cart.remove_product(product_shlapa, 2)
        assert cart.products.get(product_shlapa) == None

    def test_remove_more_products_that_avalible(self, product_book, product_shlapa, cart):
        cart.add_product(product_book, 4)
        cart.remove_product(product_book, 5)
        assert cart.products == {}
        cart.add_product(product_shlapa, 3)
        cart.remove_product(product_shlapa, 10)
        assert cart.products == {}

    def test_remove_product_no_remove_count(self, cart, product_book, product_shlapa):
        cart.add_product(product_book, 5)
        cart.remove_product(product_book)
        assert cart.products == {}
        cart.add_product(product_shlapa, 2)
        cart.remove_product(product_shlapa)
        assert cart.products == {}

    def test_clear(self, cart, product_book, product_shlapa):
        cart.add_product(product_book, 3)
        cart.add_product(product_shlapa, 1)
        cart.clear()
        assert cart.products == {}

    def test_total_price(self, cart, product_book, product_shlapa):
        cart.add_product(product_book, 4)
        cart.add_product(product_shlapa, 2)
        assert cart.get_total_price() == 2000400

    def test_buy(self, cart, product_shlapa, product_book):
        cart.add_product(product_shlapa, 1)
        cart.add_product(product_book, 5)
        cart.buy()
        assert product_shlapa.quantity == 2
        assert product_book.quantity == 995
        assert cart.products == {}

    def test_buy_more_that_available(self, cart, product_shlapa, product_book):
        cart.add_product(product_shlapa, 40)
        with pytest.raises(ValueError):
            cart.buy()
