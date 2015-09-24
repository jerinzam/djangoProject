from django.conf.urls import url
from .views import DocumentList,DocumentDetail, OrderList, OrderDetail,ShopList, ShopDetail

urlpatterns = [

	url(r'^shops/$', ShopList.as_view(), name="shop_list"),
	url(r'^shops/(?P<pk>[0-9]+)$', ShopDetail.as_view(), name="shop_detail"),
	url(r'^documents/$', DocumentList.as_view(), name="document_list"),
	url(r'^documents/(?P<pk>[0-9]+)$', DocumentDetail.as_view(), name="document_detail"),
	url(r'^orders/$', OrderList.as_view(), name="order_list"),
	url(r'^orders/(?P<pk>[0-9]+)$', OrderDetail.as_view(), name="order_detail"),

]