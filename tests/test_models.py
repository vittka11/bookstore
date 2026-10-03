from decimal import Decimal

import pytest

from tests.factories import (
    BookFactory,
    CategoryFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_category_str():
    category = CategoryFactory(name="Fantasy")

    assert str(category) == "Fantasy"


@pytest.mark.django_db
def test_book_str():
    book = BookFactory(title="Harry Potter")

    assert str(book) == "Harry Potter"


@pytest.mark.django_db
def test_book_default_stock():
    book = BookFactory(stock=10)

    assert book.stock == 10


@pytest.mark.django_db
def test_book_has_category():
    category = CategoryFactory()
    book = BookFactory(category=category)

    assert book.category == category


@pytest.mark.django_db
def test_order_str():
    order = OrderFactory(
        first_name="Vita",
        last_name="Koliada",
    )

    assert str(order) == f"Order {order.id} - Vita Koliada"


@pytest.mark.django_db
def test_order_is_not_paid_by_default():
    order = OrderFactory()

    assert order.paid is False


@pytest.mark.django_db
def test_order_item_get_cost():
    item = OrderItemFactory(
        price=Decimal("20.00"),
        quantity=3,
    )

    assert item.get_cost() == Decimal("60.00")


@pytest.mark.django_db
def test_order_item_str():
    book = BookFactory(title="Django Book")
    item = OrderItemFactory(
        book=book,
        quantity=2,
    )

    assert str(item) == "Django Book x 2"