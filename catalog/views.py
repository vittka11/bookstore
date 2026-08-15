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