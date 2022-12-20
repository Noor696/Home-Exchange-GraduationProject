from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# User model:
# Built in Django User model, an instance of this model will be created for each customer that registers with our website. 
# this model will give us the ability to later use Djangos default authentication system without having to manually set this up ourselves.

class Customer(models.Model):
    # Along with a User model each customer will contain a Customer model that holds a one to one relationship to each user .
    
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)  
	name = models.CharField(max_length=200, null=True)
	email = models.CharField(max_length=200)

	def __str__(self):
		return self.name
        # the value show in admin panel  on create a model

class Home(models.Model):
    # the Home model represents homes we have in homes list
	name = models.CharField(max_length=200)
	rooms = models.IntegerField(default=0, null=True, blank=True)
	swimming_pool = models.BooleanField(default=False,null=True, blank=True)
	parking = models.BooleanField(default=False,null=True, blank=True)
	price_day = models.FloatField()
	image = models.ImageField(null=True, blank=True)
# python -m pip install Pillow  -> run this command to accept the image
# pillow is image processing library theat allows us to add this field to our models
	def __str__(self):
		return self.name

	class Meta:
		ordering = ["-pk"]

	@property
	def imageURL(self):
		try:
			url = self.image.url
		except:
			url = 'https://papik.pro/en/uploads/posts/2022-06/1656000020_1-papik-pro-p-simple-drawings-of-my-dream-house-1.jpg'
		return url

class Booking(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_booking = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False) # if the complete is false that is an open booking we can continue adding homes to that booking , if true this a closed booking we need to create items and add them to a different booking , so this changes the status of our booking
	transaction_id = models.CharField(max_length=100, null=True)

	def __str__(self):
		return str(self.id)



	@property
	def get_booking_total(self):
		homesspecified = self.homespecified_set.all()
		total = sum([homespecified.get_total for homespecified in homesspecified])
		return total 

	@property
	def get_booking_items(self):
		homesspecified = self.homespecified_set.all()
		total = sum([homespecified.days_number for homespecified in homesspecified])
		return total 


class HomeSpecified(models.Model):
    # An home specified is one home , so far example a booking may consist of many homes but is all part of one booking. 
    # therefore the HomeSpecified model will be a child of (Home) model and the (Booking) model 
	home = models.ForeignKey(Home, on_delete=models.SET_NULL, null=True)
	booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
	days_number = models.IntegerField(default=0, null=True, blank=True)
	date_time = models.DateTimeField(null=True)
	date_added = models.DateTimeField(auto_now_add=True)
    

	def __str__(self):
		return f"Home/Hotel name : {self.home} / {self.days_number} days"
	
	@property
	def get_total(self):
		total = self.home.price_day * self.days_number
		return total

class CustomerInfo(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	booking = models.ForeignKey(Booking, on_delete=models.SET_NULL, null=True)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	phone = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address