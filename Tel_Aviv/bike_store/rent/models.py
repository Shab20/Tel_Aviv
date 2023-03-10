from django.db import models
from faker import Faker
from datetime import datetime, timedelta

# Create your models here.

class RentCustomer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Customer(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

class VehicleType(models.Model):
    name = models.CharField(max_length=50)

class VehicleSize(models.Model):
    name = models.CharField(max_length=50)

class Vehicle(models.Model):
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    date_created = models.DateField()
    real_cost = models.DecimalField(max_digits=10, decimal_places=2)
    size = models.ForeignKey(VehicleSize, on_delete=models.CASCADE)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

class Rental(models.Model):
    rental_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

class RentalRate(models.Model):
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    vehicle_size = models.ForeignKey(VehicleSize, on_delete=models.CASCADE)

class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()

def generate_customers(num_customers):
    fake = Faker()
    for i in range(num_customers):
        customer = Customer(name=fake.name(), email=fake.email())
        customer.save()

fake = Faker()

for _ in range(100):
    customer = Customer.objects.order_by('?').first()
    vehicle = Vehicle.objects.filter(is_rented=False).order_by('?').first()
    if not vehicle:
        continue
    rental_date = fake.date_time_between(start_date='-30d', end_date='now', tzinfo=None)
    return_date = None if fake.boolean(chance_of_getting_true=30) else fake.date_time_between(start_date=rental_date, end_date='now', tzinfo=None)
    rental = Rental.objects.create(
        customer=customer,
        vehicle=vehicle,
        rental_date=rental_date,
        return_date=return_date
    )
    vehicle.is_rented = True
    vehicle.save()

