
---

### **delete.md**
```markdown
```python
from bookshelf.models import Book

b1 = Book.objects.get(title="Nineteen Eighty-Four")
b1.delete()  # (1, {'bookshelf.Book': 1})
Book.objects.all()  # <QuerySet []>
