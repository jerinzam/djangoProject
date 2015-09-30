from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$',views.index,name="main"),
	url(r'^doc-list$',views.docList,name="documentList"),
	url(r'^doc-detail/(?P<docid>\d+)/$',views.docDetail,name="documentDetail"),
	url(r'^doc-edit/(?P<docid>\d+)/$',views.docEdit,name="documentEdit"),
	url(r'^doc-upload$',views.docUpload,name="documentUpload"),

]