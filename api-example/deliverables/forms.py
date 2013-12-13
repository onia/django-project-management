from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from deliverables.models import *


class DeliverableForm(ModelForm):
        class Meta:
                model = Deliverable
        def __init__(self, *args, **kwargs):
                super(DeliverableForm, self).__init__(*args, **kwargs)
