# serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Customer,Booking,Payment, Room, Hotel, Review, Staff,Amenity, Product, Category 



class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']
class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'description']

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'        

class RoomSerializer(serializers.ModelSerializer):
    # hotel = HotelSerializer()
    class Meta:
        model = Room
        fields = ['id', 'type', 'is_booked', 'room_number','hotel']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
class CustomerSerializer(serializers.ModelSerializer):
    # bookings = BookingSerializer(many=True, read_only=True)
    user=UserSerializer()
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone_number', 'name']        
class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'customer','rooms', 'check_in_date', 'check_out_date']
    
    
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_date', 'booking'] 
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['customer', 'hotel', 'rating', 'comment']

class CategorySerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name']
          
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']



    # def create(self, validated_data):
    #     user_data = validated_data.pop('user')
    #     password = user_data.pop('password')
    #     user = User.objects.create(**user_data)
    #     user.set_password(password)
    #     user.save()

        
























# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email']

    

# class CustomerSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)

#     class Meta:
#         model = Customer
#         fields = ['id', 'user', 'name']

    


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'password']
#         # extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user

# class CustomerSerializer(serializers.ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Customer
#         fields = ['user', 'name']

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user_serializer = UserSerializer(data=user_data)
        
#         if user_serializer.is_valid():
#             user = user_serializer.save()
#             customer = Customer.objects.create(user=user, **validated_data)
#             return customer
#         else:
#             raise serializers.ValidationError(user_serializer.errors)



























# class AllModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AhmarModel
#         fields = '__all__'

# class SpecificFieldsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AhmarModel
#         fields = ('name', 'age', 'email')
























