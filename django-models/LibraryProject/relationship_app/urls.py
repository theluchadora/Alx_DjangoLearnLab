from django.urls import path
from .views import list_books
from .views import LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('books/', list_books, name='list_books'),                 # Function-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),  # Class-based view

    # Authentication URLs
    # Function-based view for registration
    path('register/', views.register, name='register'),

    # Class-based login/logout using built-in views
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),


        # Role-based views
    path('admin-view/', views.admin_view, name='admin_view'),
    path('librarian-view/', views.librarian_view, name='librarian_view'),
    path('member-view/', views.member_view, name='member_view'),

        # Book permission-based views
    path('books/add_book/', views.add_book, name='add_book'),            # add book
    path('books/<int:pk>/edit_book/', views.edit_book, name='edit_book'), # edit book
    path('books/<int:pk>/delete_book/', views.delete_book, name='delete_book'), # delete book

]
