class Document(models.Model):
	doc_id = models.AutoField(primary_key=True)
	owner = models.ForeignKey('Organization',related_name='doc_owner')
	name = models.CharField(max_length=100)
	doc = models.FileField(upload_to=upload())
	tags = #used for searching docs. ee: tkm,parvathy,ECE,motor working,sem5
	display = models.BooleanField(default=True) #for delete purposes
	pages = models.IntegerField() # should be auto filled
	price = models.DecimalField(max_digits=6,decimal_places=2)# should be auto filled
	uploadedDate = models.DateTimeField(auto_now_add=True)
	updatedDate = models.DateTimeField(auto_now=True)

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

class DocCourse(models.Model):
	COURSE_CHOICES = ((ENGINEERING,'engineering'),(MCA,'MCA'),(MTECH,'MTech'))
	SEM_CHOICES = ((S1,'sem1'),(S2,'sem2'),(S3,'sem3'),(S4,'sem4'))
	document = models.ForeignKey(Document)
	course = models.CharField(max_length=50,choices=COURSE_CHOICES)
	subject = #subject based on the course chosen
	college = models.Foreignkey(College) #college table will have all the colleges
	semester = models.CharField(max_length=10,choices=SEM_CHOICES)


