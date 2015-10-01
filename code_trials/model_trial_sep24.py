from django.db import models
from django.contrib.auth.models import User
from userroles.models import UserRole

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    profile_picture = models.ImageField(upload_to='documents', null=True, blank=True)
    def __str__(self):
    	return self.user.username

class Shop(models.Model):
	shop_id = models.AutoField(primary_key=True)
	employee =  models.OneToOneField('auth.User',related_name='shop_emp')
	owner = models.ForeignKey('Organization',related_name='shop_owner')
	shopName = models.CharField(max_length=100)
	def __str__(self):
		return self.shopName

class Organization(modelsd.Model):
	owner = models.ForeignKey(User, related_name='org_owner')
	employee = models.ManyToManyField(User, related_name='org_employee',null=True,blank=True)
	def __str__(self):
		return self.owner.username

class Publisher(models.Model)
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.name

class Tag(models.Model)
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.name

class Topic(models.Model)
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.name

class University(models.Model)
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	code = models.CharField(max_length=4)
	def __str__(self):
		return self.name

class College(models.Model)
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	university = models.ForeignKey(University, null=True)
	def __str__(self):
		return self.name


class Course(models.Model)
	name = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(unique=True)
	def __str__(self):
		return self.name

class Document(models.Model):
	uuid = models.CharField(max_length=60, unique=True, blank=True)
	organization = models.ForeignKey('Organization',related_name='doc_owner', null=True, blank=True)
	private_user = models.ForeignKey(User, blank=True, null =True)
	name = models.CharField(max_length=200)
	doc = models.FileField(upload_to=upload())
	doc_type = models.ForeignKey(DocType)
	display_doc = models.FileField(upload_to="display_docs/", blank =True)
	tags = models.ManyToManyField(Tag)#used for searching docs. ee: tkm,parvathy,ECE,motor working,sem5
	topic = models.ManyToManyField(Topic, blank=True)
	display = models.BooleanField(default=True) #for delete purposes
	is_public = models.BooleanField(default=False)
	is_user_private = models.BooleanField(default=False)
	pages = models.IntegerField() # should be auto filled
	price = models.DecimalField(max_digits=6,decimal_places=2)# should be auto filled
	uploadedDate = models.DateTimeField(auto_now_add=True)
	updatedDate = models.DateTimeField(auto_now=True)
	course = models.ManyToManyField(Course, blank =True)
	edition = models.IntegerField()
	author_names = models.TextField()
	publisher = models.ForeignKey(Publisher, null =True)
	university = models.ManyToManyField(University, blank =True)


	def upload():
    	import time, random, hashlib
    	return hashlib.sha256(str(time.time())).hexdigest() +"/"

	def __str__(self):
		return self.name
	
class DocType(models.Model):
	#prefixes for variable. t- textbook,n- notes,p- project
	DOC_TYPE_CHOICES = ((NOTES,'notes'),(TEXTBOOK,'textbook'),(PROJECT,'project'))
	DOC_SHARE_CHOICES = ((PUBLIC,'public'),(PRIVATE,'private'))
	document = models.ForeignKey(Document)
	doc_type = models.CharField(max_length=20,choices=DOC_TYPE_CHOICES,default=NOTES)
	doc_share = models.CharField(max_length=5,choices=DOC_SHARE_CHOICES,default=PUBLIC) # used for sharing docs within a group
	t_author = models.CharField(max_length=50,blank=True)
	t_edition = models.IntegerField()
	t_pages = #pages included in the doc. eg: 20-24,45-55
	n_student = models.CharField(max_length=50)
	n_topic = #topics involved. eg: power,signals
	p_group = #name of the student accounts to which this doc is available

# course,subject,publisher,docType diff tables
# add foreign keys from DOCUMENT to these tables
# 

class DocCourse(models.Model):
	COURSE_CHOICES = ((ENGINEERING,'engineering'),(MCA,'MCA'),(MTECH,'MTech'))
	SEM_CHOICES = ((S1,'sem1'),(S2,'sem2'),(S3,'sem3'),(S4,'sem4'))
	document = models.ForeignKey(Document)
	course = models.CharField(max_length=50,choices=COURSE_CHOICES)
	subject = #subject based on the course chosen
	college = models.Foreignkey(College) #college table will have all the colleges
	semester = models.CharField(max_length=10,choices=SEM_CHOICES)


