from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from change_management.models import *
#from misc.widgets import DateTimeWidget
#from backends.authlib import *


class RFPCForm(ModelForm):
	class Meta:
		model = RequestForChange 
	def __init__(self, *args, **kwargs):
		super(RFPCForm, self).__init__(*args, **kwargs)
		self.fields['requestor'].widget = HiddenInput()
#		self.fields['deviceClass'].widget = HiddenInput()
