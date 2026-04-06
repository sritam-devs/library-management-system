from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.books_list),
    path('books/<str:sn>/', views.book_detail),
    path('rent/', views.rent_book),
]