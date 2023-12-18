import json
import datetime
from rest_framework.request import Request
from dateutil import parser
from rest_framework import status
from django.shortcuts import render
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Booking, Room, Hotel,Amenity, HotelAmenity, Category, Product,Passport, Person
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
# from rest_framework.permissions import AllowAny
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CustomerSerializer, UserSerializer, BookingSerializer,PaymentSerializer,PassportSerializer, PersonSerializer, RoomSerializer,HotelSerializer, ReviewSerializer, StaffSerializer, AmenitySerializer, CategorySerializer, ProductSerializer
import datetime

# class MySecureView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response({'message': 'This is a secure endpoint!'})
# @permission_classes([AllowAny])
@api_view(['POST'])
def create_customer(request):
    try:
        data = request.data

        # user_data = data.get('user', {})
        # username = data.get('username')
        data['password'] = make_password(request.data.get('password'))
        user_serializer = UserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        customer = Customer.objects.create(user=user, name=data.get('name'), phone_number=data.get('phone_number'))

        return Response({'message': 'Customer is created successfully'}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    


@api_view(['POST'])

def delete_customer(request):
    try:
        data = request.data
        username = data.get('username')

        # Retrieve the user based on the provided username
        user = User.objects.get(username=username)

        # Retrieve the customer associated with the user
        customer = Customer.objects.get(user=user)

        customer.delete()

        return JsonResponse({'message': 'Customer deleted successfully'}, status=200)

    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



# @permission_classes([IsAuthenticated])
@api_view(['POST'])
def create_booking(request):
    try:
        data = request.data
        # username = data.get('customer', {}).get('username')
        username = data.get('username')
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')
        rooms_data = data.get('rooms', [])  # Array of rooms

        check_in_date = parser.parse(check_in_date).date()
        check_out_date = parser.parse(check_out_date).date()

        if check_in_date < date.today():
            return Response({'error': 'Cannot make bookings for past dates'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(user__username=username)
        except Customer.DoesNotExist:
            return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the selected dates are available for booking
        all_bookings = Booking.objects.all()
        for booking in all_bookings:
            if (
                booking.customer.user.username != username and
                check_in_date <= booking.check_out_date and
                check_out_date >= booking.check_in_date
            ):
                return Response({'error': 'Dates are already occupied. Cannot make the booking.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a booking for each room
        for room_data in rooms_data:
            room_type = room_data.get('room_type')
            payment_amount = room_data.get('payment_amount')

            # Check for available rooms based on type
            available_rooms = Room.objects.filter(is_booked=False, type=room_type)
            if not available_rooms.exists():
                return Response({'error': f'No available rooms of that type {room_type} for the selected period'},
                                status=status.HTTP_400_BAD_REQUEST)

            selected_room = available_rooms.first()  

            # Create a booking
            booking_data = {
                "customer": customer.id,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "rooms": [selected_room.id]  
            }

            booking_serializer = BookingSerializer(data=booking_data)
            booking_serializer.is_valid(raise_exception=True)
            booking = booking_serializer.save()

            # Mark the selected room as booked
            selected_room.is_booked = True
            selected_room.save()

            # Create a payment for the booking
            payment_data = {
                "amount": payment_amount,
                "payment_date": date.today(),
                "booking": booking.id
            }

            payment_serializer = PaymentSerializer(data=payment_data)
            payment_serializer.is_valid(raise_exception=True)
            payment_serializer.save()
            
        return Response({'message': 'Bookings and payments of room created successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_bookings_by_username(request):
    
    try:
        data = request.data
        username = data.get('username')


        # Retrieve the user based on the provided username
        user = User.objects.get(username=username)

        # Retrieve the customer associated with the user
        customer = Customer.objects.get(user=user)

        # Retrieve all bookings related to the customer
        bookings = Booking.objects.filter(customer=customer)

        # Serialize the bookings
        serializer = BookingSerializer(bookings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

   
    except Customer.DoesNotExist:
        return Response({'error': 'Customer not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Customer, Booking


@api_view(['POST'])

def delete_bookings_by_username(request):
    try:
        data = request.data
        username = data.get('username')

        # Retrieve the user based on the provided username
        user = User.objects.get(username=username)

        # Retrieve the customer associated with the user
        customer = Customer.objects.get(user=user)

        # Delete all bookings related to the customer
        bookings = Booking.objects.filter(customer=customer)
        bookings.delete()

        return JsonResponse({'message': 'Bookings deleted successfully'}, status=200)

    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)



@api_view(['POST'])

def delete_specific_booking(request):
    try:
        # Use request.body to access raw JSON data
        data = request.data
        booking_id = data.get('booking_id')

        # Validate that booking_id is provided
        if booking_id is None:
            return JsonResponse({'error': 'booking_id is required in the JSON payload'}, status=400)
        # Retrieve the booking based on the provided booking_id
        booking = Booking.objects.get(id=booking_id)
        # Delete the specific booking
        booking.delete()
        return JsonResponse({'message': 'Booking deleted successfully'}, status=200)
    
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Booking not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)      



@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_room(request):
    try:
        data = request.data
        rooms_data = data.get('rooms', [])

        hotel_data = data.get('hotel', {})

        hotel_name = hotel_data.get('name')

        # Retrieve the hotel instance based on the name
        hotel_instance = Hotel.objects.get(name=hotel_name)
        
        room_data_pass = [{
            "type": room_data.get('type'),
            "is_booked": room_data.get('is_booked', False),
            "room_number": room_data.get('room_number'),
            "hotel": hotel_instance.id  
        } for room_data in rooms_data]

        room_serializer = RoomSerializer(data=room_data_pass, many=True)
        room_serializer.is_valid(raise_exception=True)
        room_serializer.save()

        return Response({'message': 'Room created successfullly'},
                        status=status.HTTP_201_CREATED)
    except Hotel.DoesNotExist:
        return Response({'error': f'Hotel with name "{hotel_name}" not found'},
                        status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_hotel(request):
    try:
        data = request.data

        # Check if amenity IDs are provided
        amenity_ids = data.pop('amenities', [])

        # Create the hotel without amenities first
        hotel_serializer = HotelSerializer(data=data)
        hotel_serializer.is_valid(raise_exception=True)
        hotel = hotel_serializer.save()

        # Associate amenities with the hotel
        for amenity_id in amenity_ids:
            try:
                amenity = Amenity.objects.get(id=amenity_id)
                HotelAmenity.objects.create(hotel=hotel, amenity=amenity)
            except Amenity.DoesNotExist:
                # Handle the case where an amenity with the provided ID doesn't exist
                pass

        return Response({'message': 'Hotel created successfully', 'Hotel_id': hotel.id},
                        status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_amenity(request):
    try:
        data = request.data

        amenity_serializer = AmenitySerializer(data=data)
        amenity_serializer.is_valid(raise_exception=True)
        amenity = amenity_serializer.save()

        return Response({'message': 'Amenity created successfully', 'Amenity_id': amenity.id},
                        status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
def amenities_by_hotel(request, hotel_id):
    try:
        hotel = get_object_or_404(Hotel, id=hotel_id)
        hotel_amenities = HotelAmenity.objects.filter(hotel=hotel)
        amenities = [hotel_amenity.amenity for hotel_amenity in hotel_amenities]
        amenity_list = [{'id': amenity.id, 'name': amenity.name} for amenity in amenities]

        return JsonResponse({'hotel_id': hotel_id, 'amenities': amenity_list})
    except Hotel.DoesNotExist:
        return JsonResponse({'error': 'Hotel not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(['GET'])

def hotels_by_amenity(request, amenity_id):
    try:
        # Get the HotelAmenity instances for the specified amenity
        hotel_amenities = HotelAmenity.objects.filter(amenity_id=amenity_id)

        # Get the hotels associated with the amenity
        hotels = [hotel_amenity.hotel for hotel_amenity in hotel_amenities]

        # Create a list of hotel details
        hotel_list = [{'id': hotel.id, 'name': hotel.name, 'address': hotel.address} for hotel in hotels]

        return JsonResponse({'amenity_id': amenity_id, 'hotels': hotel_list})
    except HotelAmenity.DoesNotExist:
        return JsonResponse({'error': 'HotelAmenity not found for the given amenity'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
        

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def create_review(request):
    try:
        data = request.data

        hotel_identifier = data.get('hotel_identifier')  
        hotel = Hotel.objects.get(name=hotel_identifier)

        # Check if a Customer with the specified username exists
        username = data.get('username')
        if Customer.objects.filter(user__username=username).exists():
            # Customer exists, allow to create a review
            review_data = {
                "customer": Customer.objects.get(user__username=username).id,
                "hotel": hotel.id,
                "rating": data.get('rating'),
                "comment": data.get('comment'),
            }

            review_serializer = ReviewSerializer(data=review_data)
            if review_serializer.is_valid():
                review_serializer.save()
                return Response({'message': 'Review created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid review data'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Customer does not exist'},
                            status=status.HTTP_403_FORBIDDEN)
    except Hotel.DoesNotExist:
        return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_staff_to_hotel(request):
    try:
        data = request.data

        hotel_identifier = data.get('hotel_identifier')
        hotel = Hotel.objects.get(name=hotel_identifier)

        staff_data_list = data.get('staff', [])
        added_staff = []

        for staff_data in staff_data_list:
            staff_data['hotel'] = hotel.id  # Set the hotel for the staff member
            staff_serializer = StaffSerializer(data=staff_data)
            if staff_serializer.is_valid():
                staff_serializer.save()
                added_staff.append(staff_serializer.data)
            else:
                return Response({'error': f'Invalid staff data: {staff_serializer.errors}'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Staff members added successfully', 'added_staff': added_staff},
                        status=status.HTTP_201_CREATED)

    except Hotel.DoesNotExist:
        return Response({'error': 'Hotel not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def add_category_with_products(request):
    try:
        data = request.data

        # Serialize category data
        category_serializer = CategorySerializer(data=data['category'])
        category_serializer.is_valid(raise_exception=True)
        category = category_serializer.save()

        # Serialize and save products with the associated category
        products_data = data.get('products', [])
        for product_data in products_data:
            product_data['category'] = category.id  # Set the category for the product
            product_serializer = ProductSerializer(data=product_data)
            product_serializer.is_valid(raise_exception=True)
            product_serializer.save()

        return Response({
            'message': 'Category and products added successfully'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_products_by_category(request, category_id):
    try:
        
        category = get_object_or_404(Category, id=category_id)
        
        products = Product.objects.filter(category=category)

        # Serialize the products
        product_serializer = ProductSerializer(products, many=True)

        return Response({'category_id': category.id, 'products': product_serializer.data})
    except Category.DoesNotExist:
        return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)        



@api_view(['GET'])
def get_category_by_product(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        category = product.category

        # Serialize the category
        category_serializer = CategorySerializer(category)

        return Response({'product_id': product.id, 'category': category_serializer.data})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def create_passport_with_person(request):
    serializer = PassportSerializer(data=request.data)
    if serializer.is_valid():
        passport = serializer.save()

        # Assuming the person data is included in the request
        person_data = request.data.get('person', {})
        person_data['passport'] = passport.id  # Associate the person with the created passport
        person_serializer = PersonSerializer(data=person_data)
        
        if person_serializer.is_valid():
            person_serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            passport.delete()  # Rollback: Delete the created passport if person creation fails
            return Response(person_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def person_by_passport(request, pass_id):
    try:
        passport = get_object_or_404(Passport, id=pass_id)
        person = get_object_or_404(Person, passport=passport)

        # Serialize the person
        person_serializer = PersonSerializer(person)

        return Response({'passport_id': passport.id, 'person': person_serializer.data})
    except Passport.DoesNotExist:
        return Response({'error': 'Passport not found'}, status=status.HTTP_404_NOT_FOUND)
    except Person.DoesNotExist:
        return Response({'error': 'Person not found for the given passport'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def passport_by_person(request, person_id):
    try:
        person = get_object_or_404(Person, id=person_id)
        passport = person.passport

        # Serialize the category
        passport_serializer = PassportSerializer(passport)

        return Response({'person_id': person.id, 'Passport': passport_serializer.data})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


