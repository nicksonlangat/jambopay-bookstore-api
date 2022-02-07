from django.db import models

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(
        max_length=250
    )
    last_name = models.CharField(
        max_length=250
    )
    email = models.EmailField(
        unique=True
    )
    date_of_birth = models.DateField()

    def __str__(self) -> str:
        return f'Author {self.first_name}, {self.last_name}'


class Book(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='book_author'
    )
    title = models.CharField(
        max_length=250
    )
    year_of_publication = models.DateField()
    description = models.TextField()
    number_of_pages = models.PositiveIntegerField()

    def __str__(self) -> str:
        return f' {self.title} by {self.author.first_name}'


class Stock(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    number_of_books_available = models.IntegerField(default=0)
    status = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return f'{self.book.title} status'

    def save(self, *args, **kwargs):

        if self.number_of_books_available <=0:
            self.status = 'Out of stock'

        elif self.number_of_books_available >= 1 and self.number_of_books_available <= 4:
            self.status = 'Critical'
        
        elif self.number_of_books_available >= 5 and self.number_of_books_available <= 9:
            self.status = 'Bad'
        
        elif self.number_of_books_available >= 10:
            self.status = 'Good'
            
        return super(Stock, self).save(*args, **kwargs)

