import pytest
from django.urls import reverse

from tests.factories import BookFactory, UserFactory


@pytest.mark.django_db
def test_book_list_view(client):
    BookFactory()

    response = client.get(reverse("catalog:book_list"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_list_contains_book(client):
    book = BookFactory(title="Harry Potter")

    response = client.get(reverse("catalog:book_list"))

    assert "Harry Potter" in response.content.decode()


@pytest.mark.django_db
def test_book_detail_view(client):
    book = BookFactory()

    response = client.get(
        reverse("catalog:book_detail", args=[book.pk])
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail_contains_title(client):
    book = BookFactory(title="Django Testing")

    response = client.get(
        reverse("catalog:book_detail", args=[book.pk])
    )

    assert "Django Testing" in response.content.decode()


@pytest.mark.django_db
def test_book_detail_not_found(client):
    response = client.get(
        reverse("catalog:book_detail", args=[99999])
    )

    assert response.status_code == 404


@pytest.mark.django_db
def test_book_create_view(client):
    response = client.get(
        reverse("catalog:book_create")
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_create_view_for_logged_in_user(client):
    user = UserFactory()
    client.force_login(user)

    response = client.get(
        reverse("catalog:book_create")
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_async_book_list(client):
    BookFactory()

    response = client.get(
        reverse("catalog:async_book_list")
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_async_book_detail(client):
    book = BookFactory()

    response = client.get(
        reverse("catalog:async_book_detail", args=[book.pk])
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_async_books_in_stock(client):
    BookFactory(stock=5)

    response = client.get(
        reverse("catalog:async_books_in_stock")
    )

    assert response.status_code == 200