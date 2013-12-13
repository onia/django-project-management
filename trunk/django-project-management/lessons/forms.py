from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from deliverables.models import *
#from misc.widgets import DateTimeWidget
#from backends.authlib import *


class LessonForm(ModelForm):
        class Meta:
                model = LessonLearnt
        def __init__(self, *args, **kwargs):
                super(LessonForm, self).__init__(*args, **kwargs)
                self.fields['author'].widget = HiddenInput()
#               self.fields['active'].widget = HiddenInput()
#               self.fields['deviceClass'].widget = HiddenInput()
