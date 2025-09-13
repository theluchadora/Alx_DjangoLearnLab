
---

### **retrieve.md**
```markdown
```python
from bookshelf.models import Book

Book.objects.all()  # <QuerySet [<Book: 1984 by George Orwell (1949)>]>
b1 = Book.objects.get(title="1984")
b1.title, b1.author, b1.publication_year  # ('1984', 'George Orwell', 1949)
