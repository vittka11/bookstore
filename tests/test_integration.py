from unittest.mock import Mock, patch

import pytest
from django.urls import reverse

from orders.models import Order
from tests.factories import BookFactory, CategoryFactory, UserFactory


@pytest.mark.django_db
def test_user_can_register(client):
    response = client.post(
        reverse("accounts:register"),
        {
            "username": "integrationuser",
            "email": "integration@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        },
    )

    assert response.status_code in (200, 302)


@pytest.mark.django_db
def test_user_can_login(client):
    UserFactory(username="testuser", password="testpass123")

    response = client.post(
        reverse("accounts:login"),
        {
            "username": "testuser",
            "password": "testpass123",
        },
    )

    assert response.status_code in (200, 302)


@pytest.mark.django_db
def test_book_list_flow(client):
    BookFactory(title="Integration Book")

    response = client.get(reverse("catalog:book_list"))

    assert response.status_code == 200
    assert "Integration Book" in response.content.decode()


@pytest.mark.django_db
def test_book_detail_flow(client):
    book = BookFactory(title="Detail Book")

    response = client.get(
        reverse("catalog:book_detail", args=[book.pk])
    )

    assert response.status_code == 200
    assert "Detail Book" in response.content.decode()


@pytest.mark.django_db
def test_create_book_flow(client):
    category = CategoryFactory()

    response = client.post(
        reverse("catalog:book_create"),
        {
            "title": "Created Book",
            "author": "Test Author",
            "price": "25.00",
            "description": "Created in integration test",
            "stock": 5,
            "category": category.pk,
        },
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_update_book_flow(client):
    book = BookFactory()
    category = book.category

    response = client.post(
        reverse("catalog:book_update", args=[book.pk]),
        {
            "title": "Updated Book",
            "author": book.author,
            "price": "30.00",
            "description": book.description,
            "stock": 7,
            "category": category.pk,
        },
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_delete_book_flow(client):
    book = BookFactory()

    response = client.post(
        reverse("catalog:book_delete", args=[book.pk])
    )

    assert response.status_code == 302


@pytest.mark.django_db
def test_add_book_to_cart(client):
    book = BookFactory()

    response = client.post(
        reverse("orders:cart_add", args=[book.pk])
    )

    assert response.status_code == 302
    assert str(book.pk) in client.session["cart"]


@pytest.mark.django_db
def test_remove_book_from_cart(client):
    book = BookFactory()

    client.post(reverse("orders:cart_add", args=[book.pk]))

    response = client.post(
        reverse("orders:cart_remove", args=[book.pk])
    )

    assert response.status_code == 302
    assert str(book.pk) not in client.session.get("cart", {})


@pytest.mark.django_db
def test_clear_cart(client):
    book = BookFactory()

    client.post(reverse("orders:cart_add", args=[book.pk]))

    response = client.post(reverse("orders:cart_clear"))

    assert response.status_code == 302
    assert client.session.get("cart") is None


@pytest.mark.django_db
def test_cart_page_contains_book(client):
    book = BookFactory(title="Cart Book")

    client.post(reverse("orders:cart_add", args=[book.pk]))

    response = client.get(reverse("orders:cart_detail"))

    assert response.status_code == 200
    assert "Cart Book" in response.content.decode()


@pytest.mark.django_db
@patch("orders.views.send_mail")
def test_checkout_creates_order_and_sends_email(mock_send_mail, client):
    book = BookFactory()
    client.post(reverse("orders:cart_add", args=[book.pk]))

    response = client.post(
        reverse("orders:order_create"),
        {
            "first_name": "Vita",
            "last_name": "Test",
            "email": "vita@example.com",
            "address": "Tirana",
        },
    )

    assert response.status_code == 302
    assert Order.objects.filter(email="vita@example.com").exists()
    mock_send_mail.assert_called_once()


@pytest.mark.django_db
@patch("orders.views.stripe.checkout.Session.create")
def test_stripe_checkout_flow(mock_stripe, client):
    book = BookFactory()
    client.post(reverse("orders:cart_add", args=[book.pk]))

    with patch("orders.views.send_mail"):
        client.post(
            reverse("orders:order_create"),
            {
                "first_name": "Vita",
                "last_name": "Test",
                "email": "stripe@example.com",
                "address": "Tirana",
            },
        )

    order = Order.objects.get(email="stripe@example.com")

    mock_stripe.return_value = Mock(
        url="https://checkout.stripe.test/session"
    )

    response = client.get(
        reverse("orders:create_checkout_session", args=[order.pk])
    )

    assert response.status_code == 302
    mock_stripe.assert_called_once()


@pytest.mark.django_db
@patch("orders.views.stripe.checkout.Session.retrieve")
def test_successful_payment_marks_order_paid(mock_retrieve, client):
    order = Order.objects.create(
        first_name="Vita",
        last_name="Test",
        email="paid@example.com",
        address="Tirana",
    )

    mock_retrieve.return_value = Mock(
        payment_status="paid",
        metadata={"order_id": str(order.id)},
    )

    response = client.get(
        reverse("orders:payment_success"),
        {"session_id": "test_session"},
    )

    order.refresh_from_db()

    assert response.status_code == 200
    assert order.paid is True


@pytest.mark.django_db
def test_payment_cancel_flow(client):
    response = client.get(
        reverse("orders:payment_cancel")
    )

    assert response.status_code == 200