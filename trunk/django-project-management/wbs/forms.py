from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from projects.misc import all_username_options, get_dependancies_for_project, get_resource_for_project
from wbs.models import *
from tinymce.widgets import TinyMCE

class DependsField(CharField):

    def clean(self, value):
        if value in ['null', '']:
            return None
        else:
            return WorkItem.objects.get(id=value)
        

class WBSUpdateField(CharField):

        def clean(self, value):
                return '''%s''' % value

class WBSProjectStage(ModelForm):

        class Meta:
                model = ProjectStage
                

class WBSReorderForm(ModelForm):

        class Meta:
                model = Project
                fields = ('work_item_order',)

        def __init__(self, *args, **kwargs):
                super(WBSReorderForm, self).__init__(*args, **kwargs)
                self.fields['work_item_order'].widget = HiddenInput()

class WBSForm(ModelForm):

        class Meta:
                model = WorkItem
                exclude = ('active', 'created_date', 'modified_date', 'wbs_number',
                                        'engineering_days', 'author')
        def __init__(self, project, *args, **kwargs):
                super(WBSForm, self).__init__(*args, **kwargs)
                self.fields['history'].widget.attrs['readonly'] = True
                self.fields['owner'].choices = get_resource_for_project(project)
                self.fields['depends'].choices = get_dependancies_for_project(project)
                self.fields['depends'] = DependsField()
                self.fields['update'] = WBSUpdateField()
                self.fields['update'].widget = Textarea()
                self.fields['update'].label = 'Update'
                self.fields['start_date'].input_formats = ['%d/%m/%Y']
                self.fields['finish_date'].input_formats = ['%d/%m/%Y']


class WBSUserForm(ModelForm):

        class Meta:
                model = WorkItem
                exclude = ('active', 'created_date', 'modified_date', 'wbs_number',
                                        'depends', 'engineering_days', 'author', 'owner', 'skill_set', 'project_phase')
        def __init__(self, project, *args, **kwargs):
                super(WBSUserForm, self).__init__(*args, **kwargs)
                self.fields['history'].widget.attrs['readonly'] = True
                self.fields['title'].widget.attrs['readonly'] = True
                self.fields['duration'].widget.attrs['disabled'] = True
                self.fields['start_date'].widget.attrs['disabled'] = True
                self.fields['finish_date'].widget.attrs['disabled'] = True
                self.fields['cost'].widget.attrs['disabled'] = True
                self.fields['description'].widget.attrs['readonly'] = True
                self.fields['update'] = WBSUpdateField()
                self.fields['update'].widget = Textarea()
                self.fields['update'].label = 'Update'





class EngineeringDayForm(ModelForm):
        class Meta:
                fields = ['work_date', 'day_type', 'resource']
                model = EngineeringDay
                #exclude = ('history',)
        def __init__(self, *args, **kwargs):
                super(EngineeringDayForm, self).__init__(*args, **kwargs)
                self.fields['resource'].choices = (('', ''),)
                self.fields['work_date'].input_formats = ['%d/%m/%Y']
        
