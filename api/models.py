from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    company_name = models.CharField(max_length=100,null=True)
    profile_picture = models.ImageField(upload_to='documents', null=True, blank=True)
    def __str__(self):
    	return user.username


class Document(models.Model):
	owner = models.ForeignKey('auth.User',related_name='documents')
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=100)
	doc = models.FileField(upload_to='documents', blank=True)
	def __str__(self):
		return self.name

class Order(models.Model):
	id = models.AutoField(primary_key=True)
	customer = models.CharField(max_length=100)
	order_doc = models.ForeignKey('Document',related_name='orders')
	status = models.CharField(max_length=20)
	shop = models.ForeignKey('UserProfile')
	comments = models.CharField(max_length=100)
	def __str__(self):
		return self.customer


