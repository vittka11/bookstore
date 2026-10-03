from django.urls import path

from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    async_book_list,
    async_book_detail,
    async_books_in_stock,
)

app_name = "catalog"

urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("book/<int:pk>/", BookDetailView.as_view(), name="book_detail"),
    path("book/add/", BookCreateView.as_view(), name="book_create"),
    path("book/<int:pk>/edit/", BookUpdateView.as_view(), name="book_update"),
    path("book/<int:pk>/delete/", BookDeleteView.as_view(), name="book_delete"),

    path("async/books/", async_book_list, name="async_book_list"),
    path("async/book/<int:pk>/", async_book_detail, name="async_book_detail"),
    path("async/in-stock/", async_books_in_stock, name="async_books_in_stock"),
]