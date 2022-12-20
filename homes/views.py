from django.shortcuts import render
from .models import *
from django.views.generic import DetailView
from django.http import JsonResponse
import json
import datetime

def homes(request):
	
	context = {}  # on context dictionary I'm going to pass some data 
	return render(request, 'homes/homes.html', context)

def home_list(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		booking, created = Booking.objects.get_or_create(customer=customer, complete=False)
		homesspecified = booking.homespecified_set.all()
		bookingH = booking.get_booking_items
	else:
		homesspecified = []
		booking = {'get_booking_total':0,'get_booking_items':0}
		bookingH = booking['get_booking_items']

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
		bookingH = booking.get_booking_items
	else:
		homesspecified = []
		booking = {'get_booking_total':0,'get_booking_items':0}
		bookingH = booking['get_booking_items']
		# customer, booking = guestOrder(request, data)
	
	context = {'homesspecified': homesspecified,
	'booking':booking , 'bookingH':bookingH
	}
	return render(request, 'homes/booking.html', context)

def checkout(request):
	if request.user.is_authenticated:
		customer = request.user.customer
		booking, created = Booking.objects.get_or_create(customer=customer, complete=False)
		homesspecified = booking.homespecified_set.all()
		bookingH = booking.get_booking_items
	else:
		homesspecified = []
		booking = {'get_booking_total':0,'get_booking_items':0}
		# customer, booking = guestOrder(request, data)
	
	context = {'homesspecified': homesspecified,
	'booking':booking , 'bookingH':bookingH
	}
	return render(request, 'homes/checkout.html', context)

def updateHome(request):
	data = json.loads(request.body)
	homeId = data['homeId']
	action = data['action']
	print('Action:', action)
	print('homeId:', homeId)

	customer = request.user.customer
	home = Home.objects.get(id=homeId)
	booking, created = Booking.objects.get_or_create(customer=customer, complete=False)

	homeSpecified, created = HomeSpecified.objects.get_or_create(booking=booking, home=home)

	if action == 'add':
		homeSpecified.days_number = (homeSpecified.days_number + 1)
	elif action == 'remove':
		homeSpecified.days_number = (homeSpecified.days_number - 1)

	homeSpecified.save()

	if homeSpecified.days_number <= 0:
		homeSpecified.delete()

	return JsonResponse('Home o Hotel was added', safe=False)

def processBooking(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		booking, created = Booking.objects.get_or_create(customer=customer, complete=False)
		total = data['form']['total']
		booking.transaction_id = transaction_id

		if total == booking.get_booking_total:
			booking.complete = True
		booking.save()
	
	# else:
	# 	customer, order = guestOrder(request, data)




	return JsonResponse('Payment submitted..', safe=False)