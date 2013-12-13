from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from risks.models import *
from wbs.forms import WBSUpdateField

class RiskForm(ModelForm):
        
    class Meta:
        model = Risk
        fields = ('description', 'owner', 'probability', 'impact', 'counter_measure', 'status', 'history')
    def __init__(self, *args, **kwargs):
        super(RiskForm, self).__init__(*args, **kwargs)
        self.fields['history'].widget.attrs['readonly'] = True
        self.fields['update'] = WBSUpdateField()
        self.fields['update'].widget = Textarea()
        self.fields['update'].label = 'Update'
