import csv
from .models import Book

def sync_to_csv():
    books = Book.objects.all()
    with open('my_books.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['serial_number', 'title', 'author', 'price'])
        for b in books:
            writer.writerow([b.serial_number, b.title, b.author, b.price])