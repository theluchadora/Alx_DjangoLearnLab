# Create Book

```python
from bookshelf.models import Book

b1 = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
