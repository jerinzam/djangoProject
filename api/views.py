from django.shortcuts import render
from rest_framework.generics import (ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response
from .models import Document, Order
from .serializers import DocumentSerializer, OrderSerializer, UserProfile
# Create your views here.


class DocumentMixin(object,):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

class DocumentList(DocumentMixin, ListCreateAPIView):
	def perform_create(self, serializer):
		# import ipdb; ipdb.set_trace()
		# url=str('/static/todoApp4/js/libs/pdfjs-1.1.215-dist/web/viewer.html?file=/static/media/documents/') + str(self.request.FILES['fileup'])
		serializer.save(owner=self.request.user)

class DocumentDetail(DocumentMixin, RetrieveUpdateDestroyAPIView):
    pass

class OrderMixin(object,):
	queryset = Order.objects.all()
	serializer_class = OrderSerializer

class OrderList(OrderMixin,ListCreateAPIView):
	def perform_create(self, serializer):
		import ipdb; ipdb.set_trace()
		# Document.objects.get(name=c)
		serializer.save(order_doc = Document.objects.get(name=self.request.data.get('name')), shop = UserProfile.objects.get(company_name=self.request.data.get('shop')))
	

class OrderDetail(OrderMixin,RetrieveUpdateDestroyAPIView):
	def perform_update(self,serializer):
		import ipdb; ipdb.set_trace()
		serializer.save(status=self.request.data.get('status'),partial=True)





