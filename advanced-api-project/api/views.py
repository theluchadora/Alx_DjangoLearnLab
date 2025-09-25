from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer
from rest_framework import filters
from django_filters import rest_framework
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

# ListView: Retrieve all books (anyone can access)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # anyone can read

    # Add filtering, searching, ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Step 1: Filtering by exact fields 
    # filterset_fields is for exact matching like i could search books/?title=Rose or /?py=1998 etc
    filterset_fields = ['title', 'author__name', 'publication_year']
    # author__name uses double underscore to filter by related Author model's name

    # Step 2: Search functionality
    # this is case insensetive and partial match like if it contains the word kind of thing
    search_fields = ['title', 'author__name']  # allows text search

    # Step 3: Ordering
    ordering_fields = ['title', 'publication_year']  # fields users can order by
    ordering = ['title']  # default ordering if none is specified

    def get_queryset(self):
        year = self.request.query_params.get('year')
        if year:
            return Book.objects.filter(publication_year=year)
        return Book.objects.all()


# DetailView: Retrieve a single book by ID (anyone can access)
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# CreateView: Add a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]  # only logged-in users

# UpdateView: Modify an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# DeleteView: Remove a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
