import json
import datetime
# from datetime import datetime
from rest_framework.request import Request
from dateutil import parser
from rest_framework import status
from django.shortcuts import render
from datetime import date
from django.http import JsonResponse
from django.contrib.auth.models import User
from decimal import Decimal
from django.db import transaction
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Customer, Booking, Room, Hotel,Amenity, HotelAmenity, Category, Product,Passport, Person,Payment
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from PIL import Image
import pytesseract




import re
from .models import UserInfo
from django.shortcuts import get_object_or_404
# from rest_framework.permissions import AllowAny
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import CustomerSerializer, UserSerializer, BookingSerializer,PaymentSerializer,PassportSerializer, PersonSerializer, RoomSerializer,HotelSerializer, ReviewSerializer, StaffSerializer, AmenitySerializer, CategorySerializer, ProductSerializer,UserInfoSerializer

# import datetimeime

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
        
        total_payment_amount = 0  # Initialize total_payment_amount outside the loop
        
        # Create a booking for each room
        for room_data in rooms_data:
            room_type = room_data.get('room_type')
            num_days = (check_out_date - check_in_date).days + 1

            # Check for available rooms based on type
            available_rooms = Room.objects.filter(is_booked=False, type=room_type)
            if not available_rooms.exists():
                return Response({'error': f'No available rooms of that type {room_type} for the selected period'},
                                status=status.HTTP_400_BAD_REQUEST)

            selected_room = available_rooms.first()  
            room_payment_amount = selected_room.price * num_days  # Calculate payment amount for the current room
            print(room_payment_amount)

            total_payment_amount += room_payment_amount  # Accumulate the total payment amount
            
            # Create a booking with the specific payment amount for the room
            booking_data = {
                "customer": customer.id,
                "check_in_date": check_in_date,
                "check_out_date": check_out_date,
                "rooms": [selected_room.id],
                "payment_amount": room_payment_amount  
            }

            booking_serializer = BookingSerializer(data=booking_data)
            booking_serializer.is_valid(raise_exception=True)
            booking = booking_serializer.save()

            # Mark the selected room as booked
            selected_room.is_booked = True
            selected_room.save()

        # Return the response after processing all rooms
        return Response({'message': f'You have booked {len(rooms_data)} rooms for {num_days} days, and your amount is {total_payment_amount}'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def process_payment(request):
    try:
        # Extract data from the request
        data = request.data
        username = data.get('username')
        booking_ids = data.get('booking_ids', [])  # List of booking IDs
        payment_amount = data.get('payment_amount')

        if not username or not booking_ids or not payment_amount:
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

        # Use transaction.atomic to ensure atomicity of the operations
        with transaction.atomic():
            payments = []  # List to store PaymentSerializer instances

            # Loop through booking_ids and create PaymentSerializer instances
            for booking_id in booking_ids:
                booking = Booking.objects.get(id=booking_id)

                # Check if the booking is already paid
                if booking.is_paid:
                    return Response({'error': f'Booking with ID {booking_id} is already paid'}, status=status.HTTP_400_BAD_REQUEST)

                # Create PaymentSerializer instance
                payment_data = {'uname': username, 'amount': payment_amount, 'booking': booking_id}
                payment_serializer = PaymentSerializer(data=payment_data)
                payment_serializer.is_valid(raise_exception=True)
                payment = payment_serializer.save()
                payments.append(payment)
                booking.is_paid = True
                booking.save() 


        return Response({'message': 'Payment processed successfully'}, status=status.HTTP_200_OK)

    except Booking.DoesNotExist:
        return Response({'error': 'One or more bookings not found'}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def cancel_booking(request):
    try:
        # Extract data from the request
        data = request.data
        username = data.get('username')
        booking_ids = data.get('booking_ids', [])

        if not username or not booking_ids:
            return Response({'error': 'Invalid request data'}, status=status.HTTP_400_BAD_REQUEST)

        # Use transaction.atomic to ensure atomicity of the operations
        with transaction.atomic():
            for booking_id in booking_ids:
                # Fetch the booking
                booking = Booking.objects.get(id=booking_id)
                if booking.is_canceled:
                    return Response({'error': f'Booking with ID {booking_id} is already canceled'}, status=status.HTTP_400_BAD_REQUEST)

                if booking.is_paid:
                    original_amount = booking.payment_amount
                    deduction_amount = Decimal(original_amount) * Decimal(0.3)
                    refund_amount = Decimal(original_amount) - deduction_amount
                    booking.payment_amount -= deduction_amount
                    booking.save()
                    
                    booking.deduction_amount=deduction_amount
                    booking.save()

                    booking.is_canceled = True
                    
                    booking.save()

                    for room in booking.rooms.all():
                        room.is_booked = False
                        room.save()

                else:
                    booking.is_canceled = True
                    booking.save()

                    for room in booking.rooms.all():
                        room.is_booked = False
                        room.save()

            return Response({'message': f'Bookings canceled successfully. Rooms made available.'}, status=status.HTTP_200_OK)

    except Booking.DoesNotExist:
        return Response({'error': 'One or more bookings not found'}, status=status.HTTP_404_NOT_FOUND)

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
            "hotel": hotel_instance.id  ,
            "price": room_data.get('price', 0.0)
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
        hotels = [hotel_amenity.hotel for hotel_amenity in hotel_amenities]
        hotel_list = [{'id': hotel.id, 'name': hotel.name, 'address': hotel.address} for hotel in hotels]

        return JsonResponse({'amenity_id': amenity_id, 'hotels': hotel_list})
    except HotelAmenity.DoesNotExist:
        return JsonResponse({'error': 'HotelAmenity not found for the given amenity'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
        

@api_view(['POST'])
def create_review(request):
    try:
        data = request.data

        hotel_identifier = data.get('hotel_identifier')  
        hotel = Hotel.objects.get(name=hotel_identifier)
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


@api_view(['POST'])
def extract_text(request, format=None):
    if request.method == 'POST':
        file_path = request.data.get('file_path')  # Replace 'username' with the actual username

        text = extract_text_from_image(file_path)
        print(text)

        user_info = parse_text(text)

        save_to_database(user_info)

        serializer = UserInfoSerializer(data=user_info)
        if serializer.is_valid():
            # Save to the database only if the serializer is valid
            save_to_database(user_info)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def extract_text_from_image(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    # print("OCR Output:", text)
    return text

def parse_text(text):

    cnic_number_match = re.search(r'\b\d{5}\s*-\s*\s*-\s*\d{7}\s*-\s*\d{1}\b', text)
    cnic_number = cnic_number_match.group(0) if cnic_number_match else None


    name_match = re.search(r'Name\s*([\w\s]+)', text)
    name = name_match.group(1).strip() if name_match else None
    
    address_match = re.search(r'Address\s*([\w\s,]+)', text)
    address = address_match.group(1).strip() if address_match else None
    
    gender_match = re.search(r'Gender\s*([\w\s]+)', text, re.IGNORECASE)
    gender = gender_match.group(1).strip() if gender_match else None

    date_match = re.search(r'\b\d{2}\.\d{2}.\d{4}\b', text)
    issue_date = date_match.group(0).strip() if date_match else None
    
    father_name_match = re.search(r'Father Name\s*([\w\s]+)', text)
    fname = father_name_match.group(1).strip() if father_name_match else None

    return {
        'cnic_number': cnic_number,
        'name': name,
        'address': address,
        'gender': gender,
        'issue_date': issue_date,
        'fname': fname,   
    }

def save_to_database(user_info):
    # Convert the 'issue_date' string to a Python datetime object
    issue_date_str = user_info['issue_date']
    issue_date = datetime.datetime.strptime(issue_date_str, '%d.%m.%Y').date() if issue_date_str else None


    new_user = UserInfo(
        cnic_number=user_info['cnic_number'],
        name=user_info['name'],
        address=user_info['address'],
        Gender=user_info['gender'],
        issue_date=issue_date,  # Use the formatted date
        fname=user_info['fname']
    )
    new_user.save()
