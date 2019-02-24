from django.db import models
from django.contrib.auth.models import User



class Restaurant(models.Model):

	name = models.CharField(max_length=50)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=50)
	logo = models.ImageField(null=True, blank=True)
	is_active = models.BooleanField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name



class Item(models.Model):

	name = models.CharField(max_length=100)
	restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='items')
	description = models.TextField(null=True, blank=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	pic = models.ImageField(null=True, blank=True)
	is_active = models.BooleanField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name