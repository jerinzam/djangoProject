from django.conf.urls import url
from . import views


urlpatterns = [

	url(r'^$',views.indexEmp,name="EmployeeMain"),
	url(r'^doc-list$',views.docList,name="documentList"),
	url(r'^doc-detail/(?P<docid>\d+)/$',views.docDetail,name="documentDetail"),
	url(r'^doc-edit/(?P<docid>\d+)/$',views.docEditSave,name="documentEdit"),
	url(r'^doc-upload$',views.docUpload,name="documentUpload"),
	url(r'^shop-profile$',views.shopProfile,name="shopProfile"),
	url(r'^shop-profile-save$',views.shopEditSave,name="shopEditSave"),
	url(r'^shop-profile/(?P<shopid>\d+)/$',views.shopProfile,name="shopProfile"),

]