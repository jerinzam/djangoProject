from django.shortcuts import render
from .models import Document
# Create your views here.

def index(request):
	docList = Document.objects.all()
	context = {"docList":docList}
	return render(request,'printo_app/index.html',context)

	
