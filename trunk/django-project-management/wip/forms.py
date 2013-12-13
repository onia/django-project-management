from django.forms import *
from wip.models import WIPItem, Heading
from projects.misc import all_company_options, get_wip_assignee_list

class WIPUpdateField(CharField):

        def clean(self, value):
                return '''%s''' % value

class WIPItemEditorForm(ModelForm):

        class Meta:
                model = WIPItem
                exclude = ('created_date', 'modified_date', 'engineering_days')

        def __init__(self, wip_report, *args, **kwargs):
                super(WIPItemEditorForm, self).__init__(*args, **kwargs)
                self.fields['history'].widget.attrs['readonly'] = True
                self.fields['update'] = WIPUpdateField()
                self.fields['update'].widget = Textarea()
                self.fields['update'].label = 'Update'
                self.fields['deadline'].input_formats = ['%d/%m/%Y']
                self.fields['assignee'].choices = get_wip_assignee_list(wip_report)


class WIPItemUserForm(ModelForm):

        class Meta:
                model = WIPItem
                exclude = ('status', 'created_date', 'modified_date', 'assignee', 'engineering_days')

        def __init__(self, *args, **kwargs):
                super(WIPItemUserForm, self).__init__(*args, **kwargs)
                self.fields['description'].widget.attrs['readonly'] = True
                self.fields['history'].widget.attrs['readonly'] = True
                self.fields['objective'].widget.attrs['disabled'] = True
                self.fields['deadline'].widget.attrs['readonly'] = True
                self.fields['complete'].widget.attrs['disabled'] = True
                self.fields['update'] = WIPUpdateField()
                self.fields['update'].widget = Textarea()
                self.fields['update'].label = 'Update'

class WIPHeadingForm(ModelForm):

        class Meta:
                model = Heading
                fields = ('company', 'heading',)
        def __init__(self, *args, **kwargs):
                super(WIPHeadingForm, self).__init__(*args, **kwargs)
                self.fields['company'].choices = all_company_options()

class CompleteWIPItemForm(ModelForm):

        class Meta:
                model = WIPItem
                fields = ('complete',)  

