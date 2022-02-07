import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .models import Author,Book,Stock
from .serializers import AuthorSerializer, BookSerializer, StockSerializer


# initialize the APIClient app
client = Client()

class CoreTest(TestCase):

    def setUp(self):
        #authors
        self.author1=Author.objects.create(
            first_name= "John",
            last_name="Kiriamiti",
            email= "johnkiriamiti@gmail.com",
            date_of_birth="1954-02-03"
            )
        self.author2=Author.objects.create(
            first_name= "Johnte",
            last_name="Kir",
            email= "johnkti@gmail.com",
            date_of_birth="1954-02-08"
            )
        self.author3=Author.objects.create(
            first_name= "May",
            last_name="June",
            email= "jct@gmail.com",
            date_of_birth="1964-02-03"
            )
        self.author4 = Author(
            first_name= "May",
            last_name="Junettt",
            email= "jct@gmjhjail.com",
            date_of_birth="1964-02-03"
        )
        #books
        self.book1=Book.objects.create(
            author=self.author1,
            title='book1',
            description='desc1',
            number_of_pages=10,
            year_of_publication="2022-02-03"
            )
        self.book2=Book.objects.create(
            author=self.author2,
            title='book2',
            description='desc2',
            number_of_pages=20,
            year_of_publication="2021-02-03"
            )
        self.book3=Book.objects.create(
            author=self.author3,
            title='book3',
            description='desc3',
            number_of_pages=30,
            year_of_publication="2019-02-03"
            )
        self.book4 = {
            'author':self.author3.pk,
            'title':'book4',
            'description':'desc4',
            'number_of_pages':30,
            'year_of_publication':"2019-02-03"
        }
        self.book4_response = client.post(
            reverse('book-list'),
            self.book4,
            format="json")

        #Stock
        self.stock1=Stock.objects.create(
            book=self.book1,
            number_of_books_available=4,
            )
        self.stock2=Stock.objects.create(
            book=self.book2,
            number_of_books_available=8,
            )
        self.stock3=Stock.objects.create(
            book=self.book3,
            number_of_books_available=12,
            )
        self.stock4 = {
            'book':self.book3.pk,
            'number_of_books_available':1
            
        }
        self.stock4_response = client.post(
            reverse('stock-list'),
            self.stock4,
            format="json")
    def test_model_can_create_an_author(self):
        old_count = Author.objects.count()
        self.author4.save()
        new_count = Author.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_get_all_authors(self):
        # get API response
        response = client.get(reverse('author-list'))
        # get data from db
        authors =Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_can_get_an_author(self):
        response = self.client.get(
            reverse('author-detail',
            kwargs={'pk': self.author1.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_invalid_author(self):
        response = self.client.get(
            reverse('author-detail',
            kwargs={'pk': 40}), format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_api_can_create_a_book(self):
        self.assertEqual(self.book4_response.status_code, status.HTTP_201_CREATED)

    def test_get_all_books(self):
        # get API response
        response = client.get(reverse('book-list'))
        # get data from db
        books =Book.objects.all()
        serializer = BookSerializer(books, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_can_get_a_book(self):
        response = self.client.get(
            reverse('book-detail',
            kwargs={'pk': self.book2.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_can_create_a_stock(self):
        self.assertEqual(self.stock4_response.status_code, status.HTTP_201_CREATED)

    def test_get_all_stock(self):
        # get API response
        response = client.get(reverse('stock-list'))
        # get data from db
        stock =Stock.objects.all()
        serializer = StockSerializer(stock, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_api_can_get_a_stock(self):
        response = self.client.get(
            reverse('stock-detail',
            kwargs={'pk': self.stock3.id}), format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    