from django.db import models

class Book(models.Model):
    serial_number = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    price = models.FloatField()

    def __str__(self):
        return self.title


class Rent(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    renter_name = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    rent_date = models.DateField(auto_now_add=True)
    amount_paid = models.FloatField()