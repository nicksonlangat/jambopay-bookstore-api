from rest_framework import serializers
from .models import Author,Book, Stock

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'date_of_birth'
        ]


class BookSerializer(serializers.ModelSerializer):
    stock_status = serializers.SerializerMethodField(read_only=True)
    stock = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Book
        fields = [
            'id',
            'author',
            'title',
            'description',
            'year_of_publication',
            'number_of_pages',
            'stock',
            'stock_status',
        ]
    
    def get_stock(self, obj):
        try:
            stock = Stock.objects.filter(book=obj).last()
            stock_available = stock.number_of_books_available
        except AttributeError:
            stock_available = 'N/A' 
        return stock_available
    
    def get_stock_status(self, obj):
        try:
            stock = Stock.objects.filter(book=obj).last()
            stock_status = stock.status
        except AttributeError:
            stock_status = 'N/A' 
        return stock_status

    def to_representation(self, instance):
        rep = super(BookSerializer, self).to_representation(instance)
        rep['author'] = f'{instance.author.first_name} {instance.author.last_name}'
        return rep


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = [
            'id',
            'book',
            'number_of_books_available',
            'status',
            
        ]
    
    def to_representation(self, instance):
        rep = super(StockSerializer, self).to_representation(instance)
        rep['book'] = f'{instance.book.title} by {instance.book.author.last_name}'
        return rep
