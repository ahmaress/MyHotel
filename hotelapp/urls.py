from django.contrib import admin
from django.urls import path

from .views import create_customer
from .views import create_room
from .views import create_hotel
from .views import create_amenity
from .views import hotels_by_amenity
from .views import create_review
from .views import add_staff_to_hotel


from .views import delete_customer
from .views import create_booking
from .views import get_bookings_by_username
from .views import delete_bookings_by_username
from .views import delete_specific_booking
# from .views import get_token


# from .views import serializerview

# from .views import createbooking
# from .views import getbooking



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/createcustomer', create_customer, name="createcustomernameee"),
    path('api/createroom', create_room, name="createroomname"),
    path('api/createhotel', create_hotel, name="createhotelname"),
    path('api/createamenity', create_amenity, name="createamenityname"),
    path('api/gethotelsbyamenity/<int:amenity_id>/', hotels_by_amenity, name="createamenityname"),


    path('api/createreview', create_review, name="createreview"),
    path('api/createstaff', add_staff_to_hotel, name="staffname"),




    # path('api/getToken', get_token, name="createcustomername"),
    path('api/deletecustomer', delete_customer, name="deletecustomername"),

    path('api/createbooking', create_booking, name="createbookingname"),
    path('api/getbookings', get_bookings_by_username, name="getcustomerbookingnamee"),
    path('api/deletebookings', delete_bookings_by_username, name="deletecustomerbookingname"),
    path('api/deleteSpecificbookings', delete_specific_booking, name="deletecustomerbookingname"),


    # path('api/customer/<int:booking_id>', createbooking, name="createbookinname"),
    # path('api/customer', getbooking, name="getbookingname")
    # path('api/serializer', serializerview, name="testserializer")


]