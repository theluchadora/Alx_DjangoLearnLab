from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Book, Author
from django.contrib.auth.models import User

class BookAPITestCase(APITestCase):

    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
        # Create authors
        self.author1 = Author.objects.create(name='Rose')
        self.author2 = Author.objects.create(name='Luchadora')

        # Create books
        self.book1 = Book.objects.create(title='Book One', publication_year=2000, author=self.author1)
        self.book2 = Book.objects.create(title='Book Two', publication_year=1997, author=self.author2)
    


    def test_list_books(self):
        url = reverse('book-list')  # /api/books/
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 2 books in setup

    def test_create_book_authenticated(self):
        url = reverse('book-create')  # /api/books/create/
        self.client.login(username='testuser', password='testpass')  # login first
        data = {
            'title': 'Book Three',
            'publication_year': 2020,
            'author': self.author1.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {'title': 'Book Four', 'publication_year': 2021, 'author': self.author2.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # should fail

    def test_update_book(self):
        url = reverse('book-update', args=[self.book1.id])
        self.client.login(username='testuser', password='testpass')
        data = {'title': 'Book One Updated', 'publication_year': 2001, 'author': self.author1.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Book One Updated')

    def test_delete_book(self):
        url = reverse('book-delete', args=[self.book2.id])
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book2.id).exists())
    
    def test_filter_by_author(self):
        url = reverse('book-list') + '?author__name=Rose'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_search_books(self):
        url = reverse('book-list') + '?search=Luchadora'
        response = self.client.get(url)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_ordering_books(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.data[0]['publication_year'], 2000)



