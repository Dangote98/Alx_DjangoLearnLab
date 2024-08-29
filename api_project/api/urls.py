from django.urls import path,include
from .views import BookList, ListCreateBookView,get_view
from .views import BookViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'bookviewset',BookViewSet,basename='bookviewset')

urlpatterns = [
    path('',include(router.urls)),
    path('api/books/create/',ListCreateBookView.as_view()),
    path('api/books/',BookList.as_view()),
    path('api/get_view/',get_view),
]
