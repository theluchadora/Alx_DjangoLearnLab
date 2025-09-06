from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from .views import register
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'),                 # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view

    # Authentication URLs
    # Function-based view for registration
    path('register/', register, name='register'),

    # Class-based login/logout using built-in views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

]
