from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response
from .models import Document, Order, Organization, UserProfile, Shop
from .serializers import DocumentSerializer, OrderSerializer, ShopSerializer
# Create your views here.

from userroles import roles

class DocumentMixin(object,):
    # queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    def get_queryset(self):
		# import ipdb; ipdb.set_trace()

	    if(self.request.user.role == roles.employee):
		    queryset = Document.objects.filter(owner=Organization.objects.get(employee=self.request.user))
	    if(self.request.user.role == roles.owner):
		    queryset = Document.objects.filter(owner=Organization.objects.get(owner=self.request.user))
	    return queryset

class DocumentList(DocumentMixin, ListCreateAPIView):
	def perform_create(self, serializer):
		
		# url=str('/static/todoApp4/js/libs/pdfjs-1.1.215-dist/web/viewer.html?file=/static/media/documents/') + str(self.request.FILES['fileup'])
		serializer.save(owner=Organization.objects.get(employee=self.request.user))

class DocumentDetail(DocumentMixin, RetrieveUpdateDestroyAPIView):
    pass

# ========================================================
class ShopMixin(object,):
	serializer_class = ShopSerializer
	def get_queryset(self):
		# import ipdb; ipdb.set_trace()
		
		if(self.request.user.role == roles.owner):
			queryset = Shop.objects.filter(owner=Organization.objects.get(owner=self.request.user))
		return queryset

class ShopList(ShopMixin,ListCreateAPIView):
	pass

class ShopDetail(ShopMixin,RetrieveUpdateDestroyAPIView):
	def perform_retrieve(self,serializer):
		import ipdb; ipdb.set_trace()
		shop = Shop.objects.get(owner)

# =========================================================



class OrderMixin(object,):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer

class OrderList(OrderMixin,ListCreateAPIView):
	def perform_create(self, serializer):
		# import ipdb; ipdb.set_trace()
		# Document.objects.get(name=c)
		serializer.save(order_doc = Document.objects.get(name=self.request.data.get('name')), shop = UserProfile.objects.get(company_name=self.request.data.get('shop')))

class OrderDetail(OrderMixin,RetrieveUpdateDestroyAPIView):
	def perform_update(self,serializer):
		# import ipdb; ipdb.set_trace()
		serializer.save(status=self.request.data.get('status'),partial=True)


# @login_required
# def shop_register(request):
		
	
# @login_required
# def upload(request):
# 	pass

# @login_required
# def edit(request, id):

# def index_shop(request):
# 	pass


# def order_list(request):
# 	pass


# def shop_detail(request, id):
# 	pass




