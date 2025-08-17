from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/lookup-isbn/', views.lookup_isbn, name='lookup_isbn'),
]
