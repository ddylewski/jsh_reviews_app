from django.urls import path
from . import views

urlpatterns = [
    path('api/lookup-isbn/', views.lookup_isbn, name='lookup_isbn'),
]
