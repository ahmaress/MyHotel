from django.contrib import admin

from .models import Customer, Booking,Payment, Room, Hotel, Review, Staff, Amenity, Product, Category


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

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1   
class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]    

admin.site.register(Hotel, HotelAdmin )
admin.site.register(Staff)
admin.site.register(Amenity)
admin.site.register(Product)
admin.site.register(Category, CategoryAdmin)




# admin.site.register(AhmarModel)

