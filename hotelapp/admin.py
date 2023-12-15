from django.contrib import admin

from .models import Customer, Booking,Payment, Room, Hotel, Review, Staff, Amenity

# Register your models here.

# class ModelHotel(admin.ModelAdmin):
#     list_display=['timee', 'status']

admin.site.register(Customer)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Room)


class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

class StaffInline(admin.TabularInline):
    model = Staff
    extra = 1    
    

class HotelAdmin(admin.ModelAdmin):
    inlines = [RoomInline, ReviewInline, StaffInline]

admin.site.register(Hotel, HotelAdmin )
admin.site.register(Staff)
admin.site.register(Amenity)




# admin.site.register(AhmarModel)

