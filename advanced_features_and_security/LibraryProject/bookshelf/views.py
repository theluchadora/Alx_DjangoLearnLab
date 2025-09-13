from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book
from .forms import ExampleForm


# Create your views here.
@login_required
@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})

@login_required
@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    # Only users with 'can_create' permission can access this view
    if request.method == "POST":
        form = ExampleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = ExampleForm()
    return render(request, "bookshelf/book_form.html", {"form": form})

@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, book_id):
    # Only users with 'can_edit' permission can access this view
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = ExampleForm(instance=book)
    return render(request, "bookshelf/book_form.html", {"form": form})


@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, book_id):
    # Only users with 'can_delete' permission can access this view
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect("book_list")

@login_required
def search_books(request):
    query = request.GET.get('q', '')
    # Use ORM filter; avoids SQL injection
    books = Book.objects.filter(title__icontains=query)
    return render(request, 'bookshelf/book_list.html', {'books': books})

