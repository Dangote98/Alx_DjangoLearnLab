from django.test import TestCase,SimpleTestCase,Client
from .models import Book,Author
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIRequestFactory,APITestCase,force_authenticate
from .views import CreateView
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.create_url = reverse('createview')
        self.update_url = reverse('updateview',args=[1])
        self.delete_url = reverse('deleteview',args=[1])
        self.new_user = User.objects.create(username='Alex',email='alex124@gmail.com',password='Alex1234.')
        self.user = User.objects.get(username='Alex')
        self.author = Author.objects.create(name='Jerr Junior')
        self.author2 = Author.objects.create(name='Rollo Tomassi')
        self.client.force_login(user=self.user)
    def test_create_new_book_POST(self):
        response = self.client.post(self.create_url,{
            'title':'The rationale male',
            'publication_year':'2011',
            'author':self.author.id
        })
        self.assertEquals(response.status_code,201)
    def test_update_book_PUT(self):
        Book.objects.create(title= 'The rationale male',
                            publication_year='2011',
                            author=self.author2)
        if Book.objects.filter(title='The rationale male').exists():
            
            response = self.client.put(self.update_url,{
                'title':'The rationale male...',
                'publication_year':'2011',
                'author':self.author2.id
            },content_type='application/json')
            
            self.assertEquals(response.status_code,200)
        else:
            print('Book not found')
            raise ValueError("Book not found")
    def test_delete_book_DELETE(self):
        Book.objects.create(title= 'The rationale male',
                            publication_year='2011',
                            author=self.author2)
        book1 = Book.objects.get(title='The rationale male')
        if book1:
            response = self.client.delete(self.delete_url, book1)
            self.assertEquals(response.status_code,204)
            
class TestViews(APITestCase):
    def setUp(self):
        
        self.factory = APIRequestFactory()
        self.new_user = User.objects.create(username='Alex',email='alex124@gmail.com',password='Alex1234.')
        self.user = User.objects.get(username='Alex')
        self.create_url = "books/create"
        self.author = Author.objects.create(name='Jerr Junior')
        self.author2 = Author.objects.create(name='Rollo Tomassi')
    def test_create_view(self):
        request = self.factory.post(self.create_url, {
            'title':'The rationale male',
            'publication_year':'2011',
            'author':self.author.id
        })
        force_authenticate(request, user=self.user)
       
        response = CreateView.as_view()(request)
        self.assertEquals(response.status_code,201)