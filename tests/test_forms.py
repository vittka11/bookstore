import pytest

from accounts.forms import CustomUserCreationForm
from orders.forms import OrderCreateForm


@pytest.mark.django_db
def test_user_registration_form_valid():
    form = CustomUserCreationForm(
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }
    )

    assert form.is_valid()


@pytest.mark.django_db
def test_user_registration_passwords_do_not_match():
    form = CustomUserCreationForm(
        data={
            "username": "newuser",
            "email": "newuser@example.com",
            "password1": "StrongPassword123!",
            "password2": "DifferentPassword123!",
        }
    )

    assert not form.is_valid()


@pytest.mark.django_db
def test_user_registration_username_required():
    form = CustomUserCreationForm(
        data={
            "username": "",
            "email": "newuser@example.com",
            "password1": "StrongPassword123!",
            "password2": "StrongPassword123!",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


def test_order_form_valid():
    form = OrderCreateForm(
        data={
            "first_name": "Vita",
            "last_name": "Koliada",
            "email": "vita@example.com",
            "address": "Tirana",
        }
    )

    assert form.is_valid()


def test_order_form_invalid_email():
    form = OrderCreateForm(
        data={
            "first_name": "Vita",
            "last_name": "Koliada",
            "email": "wrong-email",
            "address": "Tirana",
        }
    )

    assert not form.is_valid()
    assert "email" in form.errors


def test_order_form_first_name_required():
    form = OrderCreateForm(
        data={
            "first_name": "",
            "last_name": "Koliada",
            "email": "vita@example.com",
            "address": "Tirana",
        }
    )

    assert not form.is_valid()
    assert "first_name" in form.errors