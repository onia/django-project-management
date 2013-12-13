from django.forms import *
from django.contrib.admin import widgets                                       
from projects.models import *
from tinymce.widgets import TinyMCE
from projects.misc import all_username_options, all_company_options


class EditPID(ModelForm):
        
        ''' Used in templates/projects/view-project.html to edit the PID '''

        class Meta:
                model = Project
                fields = ('project_name', 'project_number', 'project_status', 'company', 'project_manager', 'team_managers', 'project_sponsor', 'project_description',
                                        'business_case', 'business_benefits', 'project_scope', 'exclusions', 'assumptions',
                                        'communications_plan', 'quality_plan', 'duration_type')

        
class DialogExecutiveSummary(ModelForm):

        ''' Used to verify executive summary / reports'''

        class Meta:
                model = ExecutiveSummary
                fields = ('summary','author','type')

        def __init__(self, *args, **kwargs):
                super(DialogExecutiveSummary, self).__init__(*args, **kwargs)
                self.fields['author'].widget = HiddenInput()
                self.fields['type'].widget = HiddenInput()


