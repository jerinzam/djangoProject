from django.db import models
from django.contrib.auth.models import User
from userroles.models import UserRole

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=100,null=True)
    profile_picture = models.ImageField(upload_to='documents', null=True, blank=True)
    def __str__(self):
    	return self.user.username

class Document(models.Model):
	doc_id = models.AutoField(primary_key=True)
	owner = models.ForeignKey('Organization',related_name='doc_owner')
	name = models.CharField(max_length=100)
	doc = models.FileField(upload_to='documents', blank=True)
	def __str__(self):
		return self.name

class Shop(models.Model):
	shop_id = models.AutoField(primary_key=True)
	employee =  models.OneToOneField('auth.User',related_name='shop_emp')
	owner = models.ForeignKey('Organization',related_name='shop_owner')
	shopName = models.CharField(max_length=100)
	def __str__(self):
		return self.shopName

class Organization(models.Model):
	org_id = models.AutoField(primary_key=True)
	owner = models.OneToOneField('auth.User', related_name='org_owner')
	employee = models.ManyToManyField('auth.User', related_name='org_employee',null=True,blank=True)
	def __str__(self):
		return self.owner.username

class Order(models.Model):
	order_id = models.AutoField(primary_key=True)
	customer = models.CharField(max_length=100)
	order_doc = models.ForeignKey('Document',related_name='order_doc')
	status = models.CharField(max_length=20)
	shop = models.ForeignKey('Shop',related_name='order_shop')
	comments = models.CharField(max_length=100)
	def __str__(self):
		return self.customer




