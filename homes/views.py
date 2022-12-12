from django.shortcuts import render

def homes(request):
	context = {}  # on context dictionary I'm going to pass some data 
	return render(request, 'homes/homes.html', context)

def booking(request):
	context = {}
	return render(request, 'homes/booking.html', context)

def checkout(request):
	context = {}
	return render(request, 'homes/checkout.html', context)
