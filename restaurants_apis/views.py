from rest_framework.generics import ListAPIView
from restaurants.models import Restaurant, Item


class RestaurantsListView(ListAPIView):
	
	queryset = Restaurant.objects.all()