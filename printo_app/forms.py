import autocomplete_light
from django import forms
from .models import Document

# class TagsAutocomplete(autocomplete_light.AutocompleteModelBase):
#     search_fields = ['name']
#     model = Tag
# autocomplete_light.register(TagsAutocomplete)

class DocUploadForm(autocomplete_light.ModelForm):
	class Meta:
		model = Document
		# widgets = {'tags' : autocomplete_light.MultipleChoiceWidget('TagAutocomplete')}
		autocomplete_fields = ('tags','topic','university',)
		exclude = ['organization','private_user','is_public','is_user_private','display']


