from django.urls import path

from . import views # (.) means in same directory

urlpatterns = [
	#Leave as empty string for base url
	path('', views.homes, name="homes"),
	path('homelist/', views.home_list, name="home_list"),
	
	path('booking/', views.booking, name="booking"),
	
	path('checkout/', views.checkout, name="checkout"),

	path('update_home/', views.updateHome, name="update_home"),
	path('process_booking/', views.processBooking, name="process_booking"),

]