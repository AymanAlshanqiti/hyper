from django.contrib import admin
from restaurants.models import Restaurant, Item

admin.site.register(Restaurant)
admin.site.register(Item)