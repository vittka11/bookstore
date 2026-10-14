import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests.factories import (
    BookFactory,
    CategoryFactory,
    OrderFactory,
    UserFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def authenticated_client(user):
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )
    return client


@pytest.fixture
def admin_client():
    admin = UserFactory(is_staff=True, is_superuser=True)
    client = APIClient()
    refresh = RefreshToken.for_user(admin)
    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
    )
    return client


# ---------------- BOOKS ----------------


@pytest.mark.django_db
def test_book_list_available_without_auth(api_client):
    BookFactory()

    response = api_client.get("/api/books/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_book_detail_available_without_auth(api_client):
    book = BookFactory()

    response = api_client.get(f"/api/books/{book.id}/")

    assert response.status_code == 200
    assert response.data["id"] == book.id


@pytest.mark.django_db
def test_book_list_contains_created_book(api_client):
    book = BookFactory(title="API Book")

    response = api_client.get("/api/books/")

    titles = [item["title"] for item in response.data["results"]]
    assert "API Book" in titles


@pytest.mark.django_db
def test_book_filter_by_author(api_client):
    BookFactory(author="Test Author")
    BookFactory(author="Other Author")

    response = api_client.get("/api/books/?author=Test%20Author")

    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_book_filter_by_category(api_client):
    category = CategoryFactory()
    BookFactory(category=category)
    BookFactory()

    response = api_client.get(
        f"/api/books/?category={category.id}"
    )

    assert response.status_code == 200
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_book_pagination(api_client):
    BookFactory.create_batch(21)

    response = api_client.get("/api/books/")

    assert response.status_code == 200
    assert len(response.data["results"]) == 20
    assert response.data["next"] is not None


@pytest.mark.django_db
def test_anonymous_cannot_create_book(api_client):
    category = CategoryFactory()

    response = api_client.post(
        "/api/books/",
        {
            "title": "New Book",
            "author": "Author",
            "price": "20.00",
            "description": "Description",
            "stock": 10,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_authenticated_non_admin_cannot_create_book(authenticated_client):
    category = CategoryFactory()

    response = authenticated_client.post(
        "/api/books/",
        {
            "title": "New Book",
            "author": "Author",
            "price": "20.00",
            "description": "Description",
            "stock": 10,
            "category": category.id,
        },
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_book(admin_client):
    book = BookFactory()

    response = admin_client.delete(f"/api/books/{book.id}/")

    assert response.status_code == 204


# ---------------- CATEGORIES ----------------


@pytest.mark.django_db
def test_category_list_available_without_auth(api_client):
    CategoryFactory()

    response = api_client.get("/api/categories/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_category_detail_available_without_auth(api_client):
    category = CategoryFactory()

    response = api_client.get(
        f"/api/categories/{category.id}/"
    )

    assert response.status_code == 200
    assert response.data["id"] == category.id


@pytest.mark.django_db
def test_anonymous_cannot_create_category(api_client):
    response = api_client.post(
        "/api/categories/",
        {
            "name": "Science",
            "slug": "science",
        },
        format="json",
    )

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_authenticated_non_admin_cannot_create_category(
    authenticated_client,
):
    response = authenticated_client.post(
        "/api/categories/",
        {
            "name": "Science",
            "slug": "science",
        },
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_category(admin_client):
    response = admin_client.post(
        "/api/categories/",
        {
            "name": "Science",
            "slug": "science",
        },
        format="json",
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_admin_can_delete_category(admin_client):
    category = CategoryFactory()

    response = admin_client.delete(
        f"/api/categories/{category.id}/"
    )

    assert response.status_code == 204


# ---------------- ORDERS ----------------


@pytest.mark.django_db
def test_anonymous_cannot_view_orders(api_client):
    response = api_client.get("/api/orders/")

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_authenticated_user_can_view_orders(authenticated_client):
    response = authenticated_client.get("/api/orders/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_order_detail_for_owner(authenticated_client, user):
    order = OrderFactory(user=user)

    response = authenticated_client.get(
        f"/api/orders/{order.id}/"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_owner_can_update_order(authenticated_client, user):
    order = OrderFactory(user=user)

    response = authenticated_client.patch(
        f"/api/orders/{order.id}/",
        {"address": "New Address"},
        format="json",
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_non_owner_cannot_update_order(authenticated_client):
    other_user = UserFactory()
    order = OrderFactory(user=other_user)

    response = authenticated_client.patch(
        f"/api/orders/{order.id}/",
        {"address": "Changed Address"},
        format="json",
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_non_owner_can_read_order(authenticated_client):
    other_user = UserFactory()
    order = OrderFactory(user=other_user)

    response = authenticated_client.get(
        f"/api/orders/{order.id}/"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_order_filter_by_paid(authenticated_client, user):
    OrderFactory(user=user, paid=True)
    OrderFactory(user=user, paid=False)

    response = authenticated_client.get(
        "/api/orders/?paid=true"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_order_filter_by_email(authenticated_client, user):
    OrderFactory(user=user, email="api@example.com")

    response = authenticated_client.get(
        "/api/orders/?email=api@example.com"
    )

    assert response.status_code == 200


# ---------------- CART ----------------


@pytest.mark.django_db
def test_anonymous_cannot_view_cart(api_client):
    response = api_client.get("/api/cart/")

    assert response.status_code in (401, 403)


@pytest.mark.django_db
def test_authenticated_user_can_view_cart(authenticated_client):
    response = authenticated_client.get("/api/cart/")

    assert response.status_code == 200


@pytest.mark.django_db
def test_add_book_to_cart(authenticated_client):
    book = BookFactory()

    response = authenticated_client.post(
        "/api/cart/add/",
        {
            "book_id": book.id,
            "quantity": 1,
        },
        format="json",
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_remove_book_from_cart(authenticated_client):
    book = BookFactory()

    authenticated_client.post(
        "/api/cart/add/",
        {
            "book_id": book.id,
            "quantity": 1,
        },
        format="json",
    )

    response = authenticated_client.post(
        "/api/cart/remove/",
        {"book_id": book.id},
        format="json",
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_clear_cart(authenticated_client):
    book = BookFactory()

    authenticated_client.post(
        "/api/cart/add/",
        {
            "book_id": book.id,
            "quantity": 1,
        },
        format="json",
    )

    response = authenticated_client.post(
        "/api/cart/clear/",
        format="json",
    )

    assert response.status_code == 200


# ---------------- JWT ----------------


@pytest.mark.django_db
def test_token_obtain(api_client):
    user = UserFactory()
    user.set_password("testpass123")
    user.save()

    response = api_client.post(
        "/api/token/",
        {
            "username": user.username,
            "password": "testpass123",
        },
        format="json",
    )

    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_token_verify(api_client):
    user = UserFactory()
    refresh = RefreshToken.for_user(user)

    response = api_client.post(
        "/api/token/verify/",
        {"token": str(refresh.access_token)},
        format="json",
    )

    assert response.status_code == 200

