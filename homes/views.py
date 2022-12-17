from django.shortcuts import render
from .models import *

def homes(request):
	
	context = {}  # on context dictionary I'm going to pass some data 
	return render(request, 'homes/homes.html', context)

def home_list(request):
	homes_list = Home.objects.all()
	context = {'homes_list' :homes_list}
	return render(request, 'homes/homes_list.html', context)

def booking(request):
	# first check if user is authenticated
	# I going to set two conditions :
	# 1. for an authenticated user.
	# 2. user that is not logged in.
	if request.user.is_authenticated:
		customer = request.user.customer
		booking, created = Booking.objects.get_or_create(customer=customer, complete=False)
		homesspecified = booking.homespecified_set.all()
	else:
		homesspecified = []
		booking = {'get_booking_total':0,'get_booking_items':0}
		# customer, booking = guestOrder(request, data)
	
	context = {'homesspecified': homesspecified,
	'booking':booking
	}
	return render(request, 'homes/booking.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		booking, created = Booking.objects.get_or_create(customer=customer, complete=False)
		homesspecified = booking.homespecified_set.all()
	else:
		homesspecified = []
		booking = {'get_booking_total':0,'get_booking_items':0}
		# customer, booking = guestOrder(request, data)
	
	context = {'homesspecified': homesspecified,
	'booking':booking
	}
	return render(request, 'homes/checkout.html', context)
