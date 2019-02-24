from rest_framework import serializers
from restaurants.models import Restaurant, Item

class RestaurantsListSerializer(serializers.ModleSerializer):
	class Meta:
		model = Restaurant
		fields = '__all__'
		