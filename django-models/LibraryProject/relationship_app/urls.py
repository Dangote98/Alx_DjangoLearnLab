from django.urls import path
from . import views
app_name = 'relationship_app'
urlpatterns = [
   path('books/', views.book_detail_view, name='books'), 
    path('<int:id>/', views.LibraryDetailView.as_view(), name='library'),
]
