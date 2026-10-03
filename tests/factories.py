import factory
from django.contrib.auth import get_user_model

from catalog.models import Category, Book
from orders.models import Order, OrderItem


User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(
        lambda obj: f"{obj.username}@example.com"
    )
    password = factory.PostGenerationMethodCall(
        "set_password",
        "testpass123"
    )


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f"Category {n}")
    slug = factory.Sequence(lambda n: f"category-{n}")


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.Sequence(lambda n: f"Book {n}")
    author = "Test Author"
    price = "20.00"
    description = "Test description"
    stock = 10
    category = factory.SubFactory(CategoryFactory)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    first_name = "Test"
    last_name = "User"
    email = "test@example.com"
    address = "Test address"


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    book = factory.SubFactory(BookFactory)
    price = "20.00"
    quantity = 1