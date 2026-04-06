from rest_framework import serializers
from .models import Book, Rent

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class RentSerializer(serializers.ModelSerializer):
    book_sn = serializers.CharField(write_only=True)

    class Meta:
        model = Rent
        fields = ['book_sn', 'renter_name', 'contact_number', 'rent_date', 'amount_paid']

    def create(self, validated_data):
        sn = validated_data.pop('book_sn')
        book = Book.objects.get(serial_number=sn)
        return Rent.objects.create(book=book, **validated_data)