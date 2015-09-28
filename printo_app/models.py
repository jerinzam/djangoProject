from django.db import models
from django.contrib.auth.models import User

import time, random,hashlib
from django.template.defaultfilters import slugify
 



class UserProfile(models.Model):
	USER_TYPE_CHOICES = ((1,'owner'),(2,'student'),(3,'Private person'))
	user = models.OneToOneField(User)
	profile_picture = models.ImageField(upload_to='documents', null=True, blank=True)
	user_type = models.IntegerField(choices='USER_TYPE_CHOICES')
	def __str__(self):
		return self.user.username

class Organization(models.Model):
	owner = models.ForeignKey(User, related_name='org_owner')
	employee = models.ManyToManyField(User, related_name='org_employee',null=True,blank=True)
	def __str__(self):
		return self.owner.username

class Shop(models.Model):
	employee =  models.ForeignKey(User,related_name='shop_employee',unique=True)
	owner = models.ForeignKey(Organization,related_name='shop_owner')
	shopName = models.CharField(max_length=100)
	def __str__(self):
		return self.shopName

class Publisher(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def save(self):
		if not self.id:
			self.slug = slugify(self.name)
			super(Publisher, self).save()
	def __str__(self):
		return self.name
	

class Tag(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def save(self):
		if not self.id:
			self.slug = slugify(self.name)
		super(Tag, self).save()
	def __str__(self):
		return self.name

class Topic(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def save(self):
		if not self.id:
			self.slug = slugify(self.name)
		super(Topic, self).save()
	def __str__(self):
		return self.name

class University(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	code = models.CharField(max_length=4)
	def save(self):
		if not self.id:
			self.slug = slugify(self.name)
		super(University, self).save()

	def __str__(self):
		return self.name

class College(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	university = models.ForeignKey(University, null=True)
	def save(self):
		if not self.id:
			self.slug = slugify(self.name)
		super(College, self).save()
	def __str__(self):
		return self.name

# ====================================================================
	# model  : COURSE
	# fields :	name - name of the course
	# 			slug - 
# ====================================================================
class Course(models.Model):
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def save(self):
		if not self.id:
			self.slug = slugify(self.name)
		super(Course, self).save()
	def __str__(self):
		return self.name

class Branch(models.Model):
	name = models.CharField(max_length=100)
	course = models.ForeignKey(Course)
	def __str__(self):
		return self.name


class DocType(models.Model):
	docType = models.CharField(max_length=20)
	slug = models.SlugField(unique=True)
	def save(self):
		if not self.id:
			self.slug = slugify(self.docType)
		super(DocType, self).save()
	def __str__(self):
		return self.docType



class Document(models.Model):
	uuid = models.CharField(max_length=60, unique=True, blank=True)
	organization = models.ForeignKey('Organization',related_name='doc_owner', null=True, blank=True)
	# shop = models.ForeignKey(Shop)
	private_user = models.ForeignKey(User, blank=True, null =True)
	name = models.CharField(max_length=200)
	# doc = models.FileField(upload_to = upload())
	doc_type = models.ForeignKey(DocType)
	pageNoRange = models.CharField(max_length=100)
	display_doc = models.FileField(upload_to="display_docs/", blank =True)
	tags = models.ManyToManyField(Tag) #used for searching docs. ee: tkm,parvathy,ECE,motor working,sem5
	topic = models.ManyToManyField(Topic, blank=True) 
	display = models.BooleanField(default=True) #for delete purposes
	is_public = models.BooleanField(default=False)
	is_user_private = models.BooleanField(default=False)
	pages = models.IntegerField() #should be auto filled
	price = models.DecimalField(max_digits=6,decimal_places=2) #should be auto filled
	uploadedDate = models.DateTimeField(auto_now_add=True) 
	updatedDate = models.DateTimeField(auto_now=True)
	course = models.ManyToManyField(Course, blank =True)
	edition = models.IntegerField(null =True, blank = True)
	author_names = models.TextField(null =True, blank = True)
	publisher = models.ForeignKey(Publisher, null =True, blank=True)
	university = models.ManyToManyField(University, blank =True)

	def upload(self):
		return hashlib.sha256(str(time.time())).hexdigest() +"/"

	def __str__(self):
		return self.name


	
