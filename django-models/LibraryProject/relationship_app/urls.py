from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import user_login
from .views import user_logout
from .views import register

urlpatterns = [
    path('books/', list_books, name='list_books'),                 # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view

    # Authentication URLs
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
]
