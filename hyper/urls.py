

from django.contrib import admin
from django.urls import path

""" Import Views's Functions """
from restaurants import views

""" Static and Media Files Setup """
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('restaurants/', views.restaurants_list, name='restaurants-list'),
    path('restaurant/<int:restaurant_id>/detail/', views.restaurant_detail, name='restaurant-detail'),

    path('restaurant/create/', views.restaurant_create, name='restaurant-create'),
    path('restaurant/<int:restaurant_id>/update/', views.restaurant_update, name='restaurant-update'),
    path('restaurant/<int:restaurant_id>/delete/', views.restaurant_delete, name='restaurant-delete'),

    path('restaurant/<int:restaurant_id>/item/create/', views.item_create, name='item-create'),
    path('item/<int:item_id>/update/', views.item_update, name='item-update'),
    path('item/<int:item_id>/create/', views.item_delete, name='item-delete'),

    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
]

""" Static and Media Files Setup """
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)