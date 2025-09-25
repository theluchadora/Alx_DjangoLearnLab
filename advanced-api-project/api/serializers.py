from rest_framework import serializers
from .models import Author, Book
import datetime

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fiels = ['id', 'title', 'publication_year', 'author']
    
    #custome validation: publication year must not be in the future
    def validate_publication_year(self, value):
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError("publication year can't be in the future")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    #nested serializer: shows all the books written by this author 
    books = BookSerializer(many= True, read_only = True)

    class Meta:
        model = Author
        fields = ['id','name', 'books']