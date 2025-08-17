# reviews/admin.py
from django.contrib import admin
from .models import Reviewer, Book, Review, Specialty

class SpecialtyAdminMixin:
    """A mixin to display many-to-many specialties in the admin list view."""
    def display_specialties(self, obj):
        """Creates a string for the specialties ManyToMany field."""
        return ", ".join(specialty.name for specialty in obj.specialties.all())
    display_specialties.short_description = 'Specialties'

class BookAdmin(admin.ModelAdmin, SpecialtyAdminMixin):
    # Updated to use the single author_name field
    list_display = ('title', 'author_name', 'status', 'display_specialties', 'publication_year')
    list_filter = ('status', 'specialties')
    search_fields = ('title', 'author_name', 'isbn')

    # Use the powerful two-box selection interface for specialties
    filter_horizontal = ('specialties',)

class ReviewerAdmin(admin.ModelAdmin, SpecialtyAdminMixin):
    list_display = ('first_name', 'last_name', 'institution', 'display_specialties', 'is_active')
    list_filter = ('institution', 'is_active', 'specialties')
    search_fields = ('first_name', 'last_name', 'institution', 'email')

    # Use the same interface for reviewers
    filter_horizontal = ('specialties',)

class ReviewAdmin(admin.ModelAdmin):
    """Custom admin options for the Review model."""
    list_display = ('book', 'reviewer', 'status', 'date_assigned', 'date_due')
    list_filter = ('status', 'reviewer')
    search_fields = ('book__title', 'reviewer__last_name', 'reviewer__first_name')
    
    # Use a more efficient widget for selecting related books and reviewers
    raw_id_fields = ('book', 'reviewer')
    date_hierarchy = 'date_assigned'

class SpecialtyAdmin(admin.ModelAdmin):
    """Custom admin options for the Specialty model."""
    search_fields = ('name',)

# Register everything with the admin site
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Reviewer, ReviewerAdmin)
admin.site.register(Review, ReviewAdmin)

# Set custom headers for the admin site
admin.site.site_header = "JSH Reviews Admin"
admin.site.site_title = "JSH Reviews Admin"
admin.site.index_title = "Admin Dashboard"