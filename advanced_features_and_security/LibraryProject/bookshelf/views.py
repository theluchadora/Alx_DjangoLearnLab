from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from .models import Book

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
        title = request.POST.get("title")
        author = request.POST.get("author")
        year = request.POST.get("publication_year")
        Book.objects.create(title=title, author=author, publication_year=year)
        return redirect("book_list")
    return render(request, "bookshelf/book_form.html")

@login_required
@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, book_id):
    # Only users with 'can_edit' permission can access this view
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author = request.POST.get("author")
        book.publication_year = request.POST.get("publication_year")
        book.save()
        return redirect("book_list")
    return render(request, "bookshelf/book_form.html", {"book": book})

@login_required
@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, book_id):
    # Only users with 'can_delete' permission can access this view
    book = get_object_or_404(Book, pk=book_id)
    book.delete()
    return redirect("book_list")

