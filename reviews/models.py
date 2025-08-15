from django.db import models

# Create your models here.
# reviews/models.py
from django.db import models
from django.utils import timezone

class Reviewer(models.Model):
    honorific = models.CharField(max_length=20, blank=True, help_text="Title such as Dr, Mr, Ms, etc.")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    post_nominals = models.CharField(max_length=50, blank=True, help_text="Credentials such as PhD, MD, etc.")
    title = models.CharField(max_length=100, blank=True, help_text="Official title, e.g., Professor of History")
    email = models.EmailField(unique=True)
    institution = models.CharField(max_length=200, blank=True)
    address_line_1 = models.CharField(max_length=255, help_text="Main street address or department name")
    address_line_2 = models.CharField(max_length=255, blank=True, help_text="Optional second line for mail stop, building, etc.")
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    class Status(models.TextChoices):
        ACQUIRED = 'ACQ', 'Acquired'
        ASSIGNED = 'ASG', 'Assigned'
        COMPLETE = 'CMP', 'Review Complete'

    title = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13, unique=True, blank=True, null=True)
    publisher = models.CharField(max_length=255, default="Unknown Publisher")
    publication_year = models.PositiveIntegerField(default=1900)
    author_name = models.CharField(max_length=255, default="Unknown Author")
    author_institution = models.CharField(max_length=255, default="Unknown Institution")
    date_received = models.DateField(default=timezone.now)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.ACQUIRED)

    def __str__(self):
        return self.title

class Review(models.Model):
    class Status(models.TextChoices):
        OFFERED = 'OFF', 'Offered'
        ACCEPTED = 'ACC', 'Accepted'
        DRAFT_RECEIVED = 'DRF', 'Draft Received'
        PUBLISHED = 'PUB', 'Published'

    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.OFFERED)
    date_assigned = models.DateField(blank=True, null=True)
    date_due = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Review for '{self.book.title}' by {self.reviewer}"