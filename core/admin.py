from django.contrib import admin

from core.models import Author, Book, Stock

# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Stock)
