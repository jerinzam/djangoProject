from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .models import Document, Organization, UserProfile, Shop
from .forms import DocUploadForm, ShopEditForm


# Create your views here.

def indexEmp(request):
	context = {'shop':shopid}
	return render(request,'index.html',context)

def docUpload(request):
	if(request.method=='POST'):
		user = UserProfile.objects.get(user=request.user)
		if(user.userType == 1 ):
			org = Organization.objects.get(owner = request.user)
		elif(user.userType == 2):
			org = Organization.objects.get(employee = request.user)
		# import ipdb;ipdb.set_trace();
		data = DocUploadForm(request.POST,request.FILES)

		new_doc = data.save(commit=False)
		new_doc.organization = org
		new_doc.is_public = True
		new_doc.save()
		data.save_m2m() 
		return HttpResponseRedirect(reverse('documentList'))
	else:
		form = DocUploadForm()
		context = { "docUploadForm" : form }
		return render(request,'printo_app/docUpload.html',context)

def docList(request):
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

def docEditSave(request,docid):
	# import ipdb;ipdb.set_trace();
	currentDoc = Document.objects.get(id=docid)
	docDetail = DocUploadForm(request.POST,request.FILES,instance=currentDoc)
	docDetail.save()	
	context = { "msg":docDetail }
	return HttpResponseRedirect(reverse('documentList'))

def shopProfile(request,shopid=None):
	# import ipdb; ipdb.set_trace()
	context = {}
	user = UserProfile.objects.get(user=request.user)
	if(user.userType == 1):
		import ipdb; ipdb.set_trace()
	elif(user.userType == 2):
		shop = Shop.objects.get(employee=request.user)
		shopForm = ShopEditForm(instance=shop)
	context = {'shopForm':shopForm}
	return render(request,'printo_app/shopProfile.html',context)

def shopEditSave(request):
	shop = Shop.objects.get(employee=request.user)
	shopForm = ShopEditForm(request.POST,instance=shop)
	shopForm.save()
	return HttpResponseRedirect(reverse('shopProfile'))

# def indexOwner(request)//

