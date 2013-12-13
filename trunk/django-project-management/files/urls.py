from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('files.views',
        (r'(?P<project_number>[-\w\./\s]+)/PID/$', 'project_pid'),
        (r'(?P<project_number>[-\w\./\s]+)/RiskRegister/$', 'risk_register'),
        (r'(?P<project_number>[-\w\./\s]+)/GanttChart/$', 'gantt_chart'),
        (r'(?P<project_number>[-\w\./\s]+)/WBS/$', 'work_breakdown_structure'),
        (r'(?P<project_number>[-\w\./\s]+)/IssueLog/$', 'issue_log'),
        (r'(?P<project_number>[-\w\./\s]+)/AddFile/$', 'add_file'),
        (r'(?P<project_number>[-\w\./\s]+)/Delete/$', 'delete_file'),
        (r'(?P<project_number>[-\w\./\s]+)/$', 'view_files'),
)

