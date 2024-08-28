from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100, null=False)
    author = models.ForeignKey(Author,on_delete=models.CASCADE, related_name='books')
    def __str__(self):
        return self.title

class Library(models.Model):
    name = models.CharField(max_length=100, null=False)
    books = models.ManyToManyField(Book, related_name='library')
    def __str__(self):
        return self.name

class Librarian(models.Model):
    name = models.CharField(max_length=100, null=False)
    library = models.OneToOneField(Library,on_delete=models.CASCADE)
    def __str__(self):
        return self.name