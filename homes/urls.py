from django.urls import path

from . import views # (.) means in same directory

urlpatterns = [
	#Leave as empty string for base url
	path('', views.homes, name="homes"),
	path('booking/', views.booking, name="booking"),
	path('checkout/', views.checkout, name="checkout"),

]