from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Document, Organization, UserProfile
from .forms import DocUploadForm
# Create your views here.

def index(request):
	
	return render(request,'index.html',{})

def docUpload(request):
	import ipdb;ipdb.set_trace();
	if(request.method=='POST'):
		user = UserProfile.objects.get(user=request.user)
		if(user.userType == 1 ):
			org = Organization.objects.get(owner = request.user)
		elif(user.userType == 2):
			org = Organization.objects.get(employee = request.user)
		import ipdb;ipdb.set_trace();
		data = DocUploadForm(request.POST,request.FILES)

		new_doc = data.save(commit=False)
		new_doc.organization = org
		new_doc.save()
		data.save_m2m() 
		return HttpResponseRedirect(reverse('documentList'))
	else:
		form = DocUploadForm()
		context = { "docUploadForm" : form }
		return render(request,'printo_app/docUpload.html',context)

def docList(request):
	# import ipdb; ipdb.set_trace()
	user = UserProfile.objects.get(user=request.user)
	if(user.userType == 1  ):
		org = Organization.objects.get(owner = request.user)
	elif(user.userType == 2):
		org = Organization.objects.get(employee = request.user)
	docList = Document.objects.filter(is_public=True).filter(organization=org)
	context = {"docs":docList}
	return render(request,'printo_app/docList.html',context)


def docDetail(request,docid):
	docDetail = Document.objects.get(id=docid)
	form = DocUploadForm(instance = docDetail)
	context = {"docEditForm":form,"doc":docDetail}
	return render(request,'printo_app/docDetail.html',context)


def docEdit(request,docid):
	import ipdb;ipdb.set_trace();
	
	docDetail = DocUploadForm(instance=Document.objects.get(id=docid))
	for (key, value) in request.POST.items():
		setattr(docDetail, key, value)
	docDetail.save()	
	context = { "doc":docDetail }
	return HttpResponseRedirect(reverse('documentList'))


