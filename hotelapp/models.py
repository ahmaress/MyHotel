from django.db import models
from django.contrib.auth.models import User


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    description = models.TextField()
    # amenities = models.ManyToManyField('Amenity', related_name='hotels')

    def __str__(self):
        return self.name
class Amenity(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
class HotelAmenity(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    amenity = models.ForeignKey(Amenity, on_delete=models.CASCADE)


class Room(models.Model):
    ROOM_TYPES = [
        ('Single', 'Single'),
        ('Double', 'Double'),
        ('Suite', 'Suite'),
    ]

    type = models.CharField(max_length=10, choices=ROOM_TYPES)
    room_number = models.CharField(max_length=10, unique=True, null=True)
    is_booked = models.BooleanField(default=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True)


    def __str__(self):
        return f" Type {self.type} {self.room_number} Room - {'Booked' if self.is_booked else 'Available'}"

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

class Staff(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    address = models.EmailField()
    jersey_number = models.CharField(max_length=10, unique=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    rating = models.IntegerField()  
    comment = models.TextField()    

    def __str__(self):
        return f"Review by {self.customer.name} for {self.hotel.name}"


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='bookings')
    rooms = models.ManyToManyField(Room, related_name='bookings')
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2,null=True)
    is_paid = models.BooleanField(default=False,null=True)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    is_canceled = models.BooleanField(default=False,null=True)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    uname = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # payment_date = models.DateField()
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment for Booking {self.booking.id}"

# models.py

from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    # product = models.OneToManyField(Product, on_delete=models.CASCADE, related_name='categories')


    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name
        # return respnse({"error":"if we you are not providing the credentials you wil"})
    
# from django.db import models

class Passport(models.Model):
    passport_number = models.CharField(max_length=20, unique=True)
    issue_date = models.DateField()
    expiration_date = models.DateField()
    country_of_issue = models.CharField(max_length=50)

    def __str__(self):
        return f'Passport {self.passport_number}'


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    passport = models.OneToOneField(Passport, on_delete=models.CASCADE, null=True, blank=True,related_name='person')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class UserInfo(models.Model):
    cnic_number = models.CharField(max_length=20,null=True)
    name = models.CharField(max_length=50,null=True)
    address = models.CharField(max_length=100,null=True)
    Gender = models.CharField(max_length=10,null=True)
    issue_date = models.DateField(null=True)   
    fname = models.CharField(max_length=50,null=True)
        


# class AhmarModel(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     email = models.EmailField()
#     address = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateField(default=datetime.date.today)
#     bio = models.TextField()


























# class Amenities(models.Model):
#     amenity_id = models.AutoField(primary_key=True)
#     amenity_name = models.CharField(max_length=255)
#     rooms = models.ManyToManyField('Room')
#     hotels = models.ManyToManyField('Hotel')

# class Booking(models.Model):
#     booking_id = models.AutoField(primary_key=True)
#     check_in_date = models.DateField()
#     check_out_date = models.DateField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     payment = models.OneToOneField('Payment', on_delete=models.CASCADE)
#     customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
#     room = models.ForeignKey('Room', on_delete=models.CASCADE)
#     guests = models.ManyToManyField('Guest')

# class Reviews(models.Model):
#     review_id = models.AutoField(primary_key=True)
#     review_text = models.TextField()
#     rating = models.IntegerField()
#     customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
#     hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)

# class Customers(models.Model):
#     customer_id = models.AutoField(primary_key=True)
#     customer_name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     bookings = models.OneToManyField('Booking')
#     reviews = models.OneToManyField('Reviews')

# class Hotel(models.Model):
#     hotel_id = models.AutoField(primary_key=True)
#     hotel_name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     reviews = models.OneToManyField('Reviews')
#     staff = models.OneToOneField('Staff', on_delete=models.CASCADE)
#     rooms = models.OneToManyField('Room')

# class Staff(models.Model):
#     staff_id = models.AutoField(primary_key=True)
#     staff_name = models.CharField(max_length=255)
#     role = models.CharField(max_length=255)
#     hotel = models.OneToOneField('Hotel', on_delete=models.CASCADE)
#     rooms = models.ManyToManyField('Room')

# class Room(models.Model):
#     room_id = models.AutoField(primary_key=True)
#     room_number = models.CharField(max_length=10)
#     room_type = models.CharField(max_length=255)
#     hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
#     bookings = models.OneToManyField('Booking')
#     staff = models.ManyToManyField('Staff')
#     amenities = models.ManyToManyField('Amenities')

# class Guest(models.Model):
#     guest_id = models.AutoField(primary_key=True)
#     guest_name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     bookings = models.ManyToManyField('Booking')

# class Payment(models.Model):
#     payment_id = models.AutoField(primary_key=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateField()
#     booking = models.OneToOneField('Booking', on_delete=models.CASCADE)

    


# class AhmarModel(models.Model):
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     email = models.EmailField()
#     address = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=15)
#     is_active = models.BooleanField(default=True)
#     date_joined = models.DateField(default=datetime.date.today)
#     bio = models.TextField()


























# class Amenities(models.Model):
#     amenity_id = models.AutoField(primary_key=True)
#     amenity_name = models.CharField(max_length=255)
#     rooms = models.ManyToManyField('Room')
#     hotels = models.ManyToManyField('Hotel')

# class Booking(models.Model):
#     booking_id = models.AutoField(primary_key=True)
#     check_in_date = models.DateField()
#     check_out_date = models.DateField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     payment = models.OneToOneField('Payment', on_delete=models.CASCADE)
#     customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
#     room = models.ForeignKey('Room', on_delete=models.CASCADE)
#     guests = models.ManyToManyField('Guest')

# class Reviews(models.Model):
#     review_id = models.AutoField(primary_key=True)
#     review_text = models.TextField()
#     rating = models.IntegerField()
#     customer = models.ForeignKey('Customers', on_delete=models.CASCADE)
#     hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)

# class Customers(models.Model):
#     customer_id = models.AutoField(primary_key=True)
#     customer_name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     bookings = models.OneToManyField('Booking')
#     reviews = models.OneToManyField('Reviews')

# class Hotel(models.Model):
#     hotel_id = models.AutoField(primary_key=True)
#     hotel_name = models.CharField(max_length=255)
#     location = models.CharField(max_length=255)
#     reviews = models.OneToManyField('Reviews')
#     staff = models.OneToOneField('Staff', on_delete=models.CASCADE)
#     rooms = models.OneToManyField('Room')

# class Staff(models.Model):
#     staff_id = models.AutoField(primary_key=True)
#     staff_name = models.CharField(max_length=255)
#     role = models.CharField(max_length=255)
#     hotel = models.OneToOneField('Hotel', on_delete=models.CASCADE)
#     rooms = models.ManyToManyField('Room')

# class Room(models.Model):
#     room_id = models.AutoField(primary_key=True)
#     room_number = models.CharField(max_length=10)
#     room_type = models.CharField(max_length=255)
#     hotel = models.ForeignKey('Hotel', on_delete=models.CASCADE)
#     bookings = models.OneToManyField('Booking')
#     staff = models.ManyToManyField('Staff')
#     amenities = models.ManyToManyField('Amenities')

# class Guest(models.Model):
#     guest_id = models.AutoField(primary_key=True)
#     guest_name = models.CharField(max_length=255)
#     email = models.EmailField()
#     phone = models.CharField(max_length=15)
#     bookings = models.ManyToManyField('Booking')

# class Payment(models.Model):
#     payment_id = models.AutoField(primary_key=True)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     payment_date = models.DateField()
#     booking = models.OneToOneField('Booking', on_delete=models.CASCADE)
