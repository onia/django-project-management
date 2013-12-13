from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from files.models import *


class FileForm(ModelForm):
        class Meta:
                model = ProjectFile
        def __init__(self, *args, **kwargs):
                super(FileForm, self).__init__(*args, **kwargs)
                self.fields['author'].widget = HiddenInput()
