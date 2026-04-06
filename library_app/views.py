from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book
from .serializers import BookSerializer
from .utils import sync_to_csv
from .models import Book, Rent
from .serializers import BookSerializer, RentSerializer

@api_view(['GET', 'POST'])
def books_list(request):
    if request.method == 'GET':
        author = request.GET.get('author')
        title = request.GET.get('title')

        books = Book.objects.all()

        if author:
            books = books.filter(author__icontains=author)
        if title:
            books = books.filter(title__icontains=title)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            sync_to_csv()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)


@api_view(['GET', 'PATCH', 'DELETE'])
def book_detail(request, sn):
    try:
        book = Book.objects.get(serial_number=sn)
    except Book.DoesNotExist:
        return Response({'error': 'Not found'}, status=404)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)

    if request.method == 'PATCH':
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            sync_to_csv()
            return Response(serializer.data)

    if request.method == 'DELETE':
        book.delete()
        sync_to_csv()
        return Response({'message': 'Deleted'})
    
def home(request):
    return render(request, 'index.html')

@api_view(['POST', 'GET'])
def rent_book(request):
    if request.method == 'POST':
        serializer = RentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if request.method == 'GET':
        rents = Rent.objects.select_related('book').all()
        data = []
        for r in rents:
            data.append({
                'serial_number': r.book.serial_number,
                'title': r.book.title,
                'renter_name': r.renter_name,
                'contact_number': r.contact_number,
                'rent_date': r.rent_date,
                'amount_paid': r.amount_paid
            })
        return Response(data)