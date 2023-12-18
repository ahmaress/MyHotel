from django.contrib import admin
from django.urls import path

from .views import create_customer
from .views import create_room
from .views import create_hotel
from .views import create_amenity
# from .views import create_person_with_passport
from .views import create_passport_with_person

from .views import hotels_by_amenity
from .views import create_review
from .views import get_category_by_product
from .views import add_staff_to_hotel
from .views import get_products_by_category
from .views import add_category_with_products
from .views import amenities_by_hotel
from .views import delete_customer
from .views import passport_by_person
from .views import person_by_passport
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
    # path('api/createpersonpassport', create_person_with_passport, name="createpersonpassport"),
    path('api/createpassportperson', create_passport_with_person, name="createpersonpassport"),
    path('api/personbypassport/<int:pass_id>/', person_by_passport, name="creategetproductbycategory"),
    path('api/passbyperson/<int:person_id>/', passport_by_person, name="creategetproductbycategory"),



    

    path('api/createhotel', create_hotel, name="createhotelname"),
    path('api/createamenity', create_amenity, name="createamenityname"),
    path('api/createproduct', add_category_with_products, name="createamenityname"),

    path('api/gethotelsbyamenity/<int:amenity_id>/', hotels_by_amenity, name="createamenityname"),
    path('api/getamenitybyhotel/<int:hotel_id>/', amenities_by_hotel, name="createamenityname"),
    path('api/get_products_by_category/<int:category_id>/', get_products_by_category, name="creategetproductbycategory"),
    path('api/get_category_by_product/<int:product_id>/', get_category_by_product, name="creategetproductbycategory"),





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