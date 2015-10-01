import autocomplete_light
from django import forms
from .models import Document, Shop

# class TagsAutocomplete(autocomplete_light.AutocompleteModelBase):
#     search_fields = ['name']
#     model = Tag
# autocomplete_light.register(TagsAutocomplete)
class ReadOnlyFieldsMixin(object):
    readonly_fields = ()
    all_fields = False

    def __init__(self, *args, **kwargs):
        super(ReadOnlyFieldsMixin, self).__init__(*args, **kwargs)
        if len(self.readonly_fields) == 0:
            self.all_fields = True
        else:
            self.all_fields = False

        for field in (field for field_name, field in six.iteritems(self.fields)
                      if field_name in self.readonly_fields
                      or self.all_fields is True):
            field.widget.attrs['disabled'] = 'true'
            field.required = False

    def clean(self):
        cleaned_data = super(ReadOnlyFieldsMixin, self).clean()
        if self.all_fields:
            for field_name, field in six.iteritems(self.fields):
                cleaned_data[field_name] = getattr(self.instance, field_name)
            return cleaned_data
        else:
            for field_name in self.readonly_fields:
                cleaned_data[field_name] = getattr(self.instance, field_name)
            return cleaned_data

class DocUploadForm(autocomplete_light.ModelForm):
	class Meta:
		model = Document
		# widgets = {'tags' : autocomplete_light.MultipleChoiceWidget('TagAutocomplete')}
		autocomplete_fields = ('tags','topic','university',)
		exclude = ['organization','private_user','is_public','is_user_private','display']

class ShopEditForm(autocomplete_light.ModelForm):
	# owner = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
	# readonly_fields = ('owner',)
	# widgets = {'owner':/ forms.widgets.Select(attrs={'readonly': True,'disabled': True})}
	# employee = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
	class Meta:
		model = Shop
		widgets = {
      		'owner' : forms.HiddenInput(),
  			'employee' : forms.HiddenInput(),
  			'shopName' : forms.HiddenInput()
     	}
		# read_only = ('shopName')
		# widgets = {'tags' : autocomplete_light.MultipleChoiceWidget('TagAutocomplete')}
		autocomplete_fields = ('services',)
		exclude = ['',]


