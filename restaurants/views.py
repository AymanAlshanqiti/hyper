
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.db.models import Q
from restaurants.models import Restaurant, Item
from restaurants.forms import SignupForm, SigninForm, RestaurantForm, ItemForm



""" #################### Auth Functions #################### """

def signup(request):

	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			user_obj = form.save(commit=False)
			user_obj.set_password(user_obj.password) 
			user_obj.save()

			login(request, user_obj)
			return redirect('restaurants-list')


	context = {
		'form': form,
	}
	return render(request, 'auth/signup.html', context)
	


def signin(request):

	form = SigninForm()
	if request.method == 'POST':
		form = SigninForm(request.POST)
		if form.is_valid():
			my_username = form.cleaned_data['username']
			my_password = form.cleaned_data['password']

			user_obj = authenticate(username=my_username, password=my_password)
			if user_obj is not None:
				login(request, user_obj)
				return redirect('restaurants-list')

			messages.success(request, "Wrong data")

	context = {
		'form': form,
	}
	return render(request, 'auth/signin.html', context)



def signout(request):
	logout(request)
	return redirect('signin')





""" #################### Restaurant Functions #################### """

def restaurants_list(request):
	
	restaurants = Restaurant.objects.all()

	query = request.GET.get("q")
	if query:
		restaurants = restaurants.filter(
			Q(name__icontains = query)|
			Q(owner__first_name__icontains = query)|
			Q(status__icontains = query)
		).distinct()

	context = {
		'restaurants': restaurants
	}
	return render(request, 'restaurants/list.html', context)



def restaurant_detail(request, restaurant_id):
	
	restaurant = Restaurant.objects.get(id=restaurant_id)
	items = restaurant.items.all().order_by('is_active', 'price')
	context = {
		'restaurant': restaurant,
		'items': items,
	}
	return render(request, 'restaurants/detail.html', context)



def restaurant_create(request):

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('signin')
	
	form = RestaurantForm()
	if request.method == "POST":
		form = RestaurantForm(request.POST, request.FILES)
		if form.is_valid():
			restaurant = form.save(commit=False)
			restaurant.owner = request.user
			restaurant.save()

			messages.success(request, "Successfully Created!")
			return redirect('restaurants-list')

	context = {
		'form': form,
	}
	return render(request, 'restaurants/create.html', context)



def restaurant_update(request, restaurant_id):

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('signin')

	restaurant = Restaurant.objects.get(id=restaurant_id)
	if not (restaurant.owner == request.user):
		messages.success(request, 'Restaurant\'s owner only has a permission to update this restaurant info!')
		return redirect('restaurants-list')

	form = RestaurantForm(instance=restaurant)
	if request.method == 'POST':
		form = RestaurantForm(request.POST, request.FILES, instance=restaurant)
		if form.is_valid():
			form.save()
			messages.success(request, 'Successfully updated!')
			return redirect('restaurants-list')

	context = {
		'form': form,
		'restaurant': restaurant,
	}
	return render(request, 'restaurants/update.html', context)



def restaurant_delete(request, restaurant_id):

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('signin')

	restaurant = Restaurant.objects.get(id=restaurant_id)
	if not (restaurant.owner == request.user):

		messages.success(request, 'Restaurant\'s owner only has a permission to delete this restaurant!')
		return redirect('restaurants-list')

	restaurant.delete()
	messages.success(request, 'Successfully deleted!')
	return redirect('restaurants-list')





""" #################### Item Functions #################### """

def item_create(request, restaurant_id):

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('signin')

	restaurant = Restaurant.objects.get(id=restaurant_id)

	if restaurant.owner != request.user:
		messages.success(request, 'Restaurant\'s owner only has a permission to add items!')
		return redirect('restaurant-detail', restaurant_id)
	
	form = ItemForm()
	if request.method == "POST":
		form = ItemForm(request.POST, request.FILES)
		if form.is_valid():
			item = form.save(commit=False)
			item.restaurant = restaurant
			item.save()

			messages.success(request, "Successfully Created!")
			return redirect('restaurant-detail', restaurant_id)

	context = {
		'form': form,
		'restaurant': restaurant,
	}
	return render(request, 'items/create.html', context)



def item_update(request, item_id):

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('signin')

	item = Item.objects.get(id= item_id)

	if item.restaurant.owner != request.user:
		messages.success(request, 'Restaurant\'s owner only has a permission to update item!')
		return redirect('restaurant-detail', restaurant_id=item.restaurant.id)


	form = ItemForm(instance=item)
	if request.method == 'POST':
		form = ItemForm(request.POST, request.FILES, instance=item)
		if form.is_valid():
			form.save()

			messages.success(request, 'Successfully updated!')
			return redirect('restaurant-detail', restaurant_id=item.restaurant.id)

	context = {
		'form': form,
		'item': item,
	}
	return render(request, 'items/update.html', context)



def item_delete(request, item_id):

	item = Item.objects.get(id=item_id)

	if request.user.is_anonymous:
		messages.success(request, 'You have to signin first!')
		return redirect('signin')

	restaurant = Restaurant.objects.get(id=item.restaurant.id)
	print(restaurant)
	if not (restaurant.owner == request.user):

		messages.success(request, 'Restaurant\'s owner only has a permission to delete this item!')
		return redirect('restaurant-detail', restaurant_id=item.restaurant.id)

	item.delete()
	messages.success(request, 'Successfully deleted!')
	return redirect('restaurant-detail', restaurant_id=item.restaurant.id)











