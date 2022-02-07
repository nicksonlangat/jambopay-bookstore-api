from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Author, Book, Stock
from .serializers import AuthorSerializer, BookSerializer, StockSerializer

# Create your views here.

class AuthorViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['email', 'first_name', 'last_name']
    filterset_fields = ['email', 'first_name', 'last_name']


class BookViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['author__email', 'author__first_name', 'author__last_name', 'title', 'year_of_publication']
    filterset_fields = ['author__id', 'id', 'title', 'year_of_publication']


class StockViewset(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['book__title', 'book__id','status']
    filterset_fields = ['book__title', 'book__id','status']

    def destroy(self, request, *args, **kwargs):
        return Response(data='Stock cannot be removed', status=status.HTTP_403_FORBIDDEN)
        

