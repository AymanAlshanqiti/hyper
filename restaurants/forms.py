from django import forms
from restaurants.models import Restaurant, Item
from django.contrib.auth.models import User


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'status', 'logo', 'is_active']



class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'password']

		widgets = {
			'password': forms.PasswordInput()
		}
		


class SigninForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput())



class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		exclude = ['restaurant']