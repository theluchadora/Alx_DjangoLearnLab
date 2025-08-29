
---

### **update.md**
```markdown
```python
from bookshelf.models import Book

b1 = Book.objects.get(title="1984")
b1.title = "Nineteen Eighty-Four"
b1.save()
Book.objects.all()  # <QuerySet [<Book: Nineteen Eighty-Four by George Orwell (1949)>]>
