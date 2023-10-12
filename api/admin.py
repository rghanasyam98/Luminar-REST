from django.contrib import admin

# Register your models here.

from .models import Product,Book,Publisher,Genre,Country,Author,Cart,Review

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Review)

admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Genre)
admin.site.register(Country)
admin.site.register(Author)



