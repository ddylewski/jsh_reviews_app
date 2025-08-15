from django.contrib import admin

# Register your models here.
# reviews/admin.py
from django.contrib import admin
from .models import Reviewer, Book, Review


# Define a custom ModelAdmin for the Book model
class BookAdmin(admin.ModelAdmin):
	change_form_template = "admin/reviews/book/change_form.html"
	list_display = ('title', 'author_name', 'publisher', 'status', 'date_received')
	list_filter = ('status',)
	search_fields = ('title', 'author_name', 'isbn', 'publisher')

admin.site.register(Book, BookAdmin)
admin.site.register(Reviewer)
admin.site.register(Review)