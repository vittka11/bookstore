from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Book


class BookListView(ListView):
    """Display a paginated list of books."""
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 5


class BookDetailView(DetailView):
    """Display detailed information about a single book."""
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"

class BookCreateView(CreateView):
    """Display a form and create a new book."""
    model = Book
    fields = ["title", "author", "price", "description", "stock", "category"]
    template_name = "catalog/book_form.html"
    success_url = "/"    

class BookUpdateView(UpdateView):
    """Display a form and update an existing book."""
    model = Book
    fields = ["title", "author", "price", "description", "stock", "category"]
    template_name = "catalog/book_form.html"
    success_url = "/"    

class BookDeleteView(DeleteView):
    """Delete an existing book after confirmation."""
    model = Book
    template_name = "catalog/book_confirm_delete.html"
    success_url = "/"    

async def async_book_list(request):
    """Display the book list using an asynchronous database query."""
    books = [
        book
        async for book in Book.objects.select_related("category").all()
    ]

    return await sync_to_async(render)(
        request,
        "catalog/book_list.html",
        {"books": books},
    )
async def async_book_detail(request, pk):
    """Display a single book using an asynchronous database query."""
    book = await Book.objects.select_related("category").aget(pk=pk)

    return await sync_to_async(render)(
        request,
        "catalog/book_detail.html",
        {"book": book},
    )    
async def async_books_in_stock(request):
    """Display in-stock books using an asynchronous database query."""
    books = [
        book
        async for book in Book.objects.filter(stock__gt=0)
        .select_related("category")
    ]

    return await sync_to_async(render)(
        request,
        "catalog/book_list.html",
        {"books": books},
    )