from django.shortcuts import render, redirect
from .models import *

from django.http import JsonResponse
import json
import datetime

from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home_list')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('login')




	context = {'form':form}
	return render(request, 'homes/register.html', context)

		

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home_list')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')
			user = authenticate(request, username=username, password=password)
			
			if user is not None:
				login(request, user)
				return redirect('home_list')
			else:
				messages.info(request, 'Username OR password is incorrect')


	context = {}
	return render(request, 'homes/login.html', context)

	
	

def logoutUser(request):
	
	logout(request)
	return redirect('homes')


def homes(request):
	
	context = {}  # on context dictionary I'm going to pass some data 
	return render(request, 'homes/homes.html', context)

@login_required(login_url='login')
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



@login_required(login_url='login')
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

@login_required(login_url='login')
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