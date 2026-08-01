from django.contrib import admin
from .models import Book, Category


class BookInline(admin.TabularInline):
    model = Book
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = [BookInline]
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'stock')
    list_filter = ('author',)
    search_fields = ('title', 'author')
