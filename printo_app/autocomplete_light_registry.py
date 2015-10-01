import autocomplete_light.shortcuts as al
from .models import Document, Tag, Topic, University, Service
import autocomplete_light
from django import http


class ServiceAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = Service
	search_fields = ['name',]
	attrs={
	    'placeholder': 'Please enter your services',
	    'data-autocomplete-minimum-characters': 1,
	}
	widget_attrs={
		'autocomplete' : 'remote',
		'data-widget-bootstrap':'rest_model',
	    'data-widget-maximum-values': 4,
	    'class': 'modern-style',
	}
	def autocomplete_html(self):
	    html = super(ServiceAutocomplete, self).autocomplete_html()
	    html += '<span data-value=000>Create New TAG</span>'
	    return html

	def post(self, request, *args, **kwargs):
		# import ipdb; ipdb.set_trace();
		new_service = Service()
		new_service.name = request.POST['name']
		new_service.save()
		return http.HttpResponse(new_service.pk)

class TagAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = Tag
	search_fields = ['name',]
	attrs={
	    'placeholder': 'Please enter related tags?',
	    'data-autocomplete-minimum-characters': 1,
	}
	widget_attrs={
		'autocomplete' : 'remote',
		'data-widget-bootstrap':'rest_model',
	    'data-widget-maximum-values': 4,
	    'class': 'modern-style',
	}
	def autocomplete_html(self):
	    html = super(TagAutocomplete, self).autocomplete_html()
	    html += '<span data-value=000>Create New TAG</span>'
	    return html

	def post(self, request, *args, **kwargs):
		# import ipdb; ipdb.set_trace();
		new_tag = Tag()
		new_tag.name = request.POST['name']
		new_tag.save()
		return http.HttpResponse(new_tag.pk)

class TopicAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = Topic
	search_fields = ['name',]
	attrs={
	    'placeholder': 'Please enter related topic tags',
	    'data-autocomplete-minimum-characters': 1,
	}
	widget_attrs={
		'autocomplete' : 'remote',
		'data-widget-bootstrap':'rest_model',
	    'data-widget-maximum-values': 4,
	    'class': 'modern-style',
	}
	def autocomplete_html(self):
	    html = super(TopicAutocomplete, self).autocomplete_html()
	    html += '<span data-value=000>Create New TAG</span>'
	    return html

	def post(self, request, *args, **kwargs):
		# import ipdb; ipdb.set_trace();
		new_topic = Topic()
		new_topic.name = request.POST['name']
		new_topic.save()
		return http.HttpResponse(new_topic.pk)

class UniversityAutocomplete(autocomplete_light.AutocompleteModelBase):
	model = University
	search_fields = ['name',]
	attrs={
	    'placeholder': 'Please enter the University',
	    'data-autocomplete-minimum-characters': 1,
	}
	widget_attrs={

	    'data-widget-maximum-values': 1,
	    'class': 'modern-style',
	}


autocomplete_light.register(Service,ServiceAutocomplete)
autocomplete_light.register(Tag,TagAutocomplete)
autocomplete_light.register(Topic,TopicAutocomplete)
autocomplete_light.register(University,UniversityAutocomplete)