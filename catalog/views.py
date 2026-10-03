from asgiref.sync import sync_to_async
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Book


class BookListView(ListView):
    model = Book
    template_name = "catalog/book_list.html"
    context_object_name = "books"
    paginate_by = 5


class BookDetailView(DetailView):
    model = Book
    template_name = "catalog/book_detail.html"
    context_object_name = "book"

class BookCreateView(CreateView):
    model = Book
    fields = ["title", "author", "price", "description", "stock", "category"]
    template_name = "catalog/book_form.html"
    success_url = "/"    

class BookUpdateView(UpdateView):
    model = Book
    fields = ["title", "author", "price", "description", "stock", "category"]
    template_name = "catalog/book_form.html"
    success_url = "/"    

class BookDeleteView(DeleteView):
    model = Book
    template_name = "catalog/book_confirm_delete.html"
    success_url = "/"    

async def async_book_list(request):
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
    book = await Book.objects.select_related("category").aget(pk=pk)

    return await sync_to_async(render)(
        request,
        "catalog/book_detail.html",
        {"book": book},
    )    
async def async_books_in_stock(request):
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