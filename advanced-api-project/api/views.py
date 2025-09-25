from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# Create your views here.

# ListView: Retrieve all books (anyone can access)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # anyone can read

    def get_queryset(self):
        year = self.request.query_params.get('year')
        if year:
            return Book.objects.filter(publication_year=year)
        return Book.objects.all()


# DetailView: Retrieve a single book by ID (anyone can access)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# CreateView: Add a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # only logged-in users

# UpdateView: Modify an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# DeleteView: Remove a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
