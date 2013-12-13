from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('issues.views',
        (r'(?P<project_number>[-\w\./\s]+)/(?P<issue_id>[-\w\./\s]+)/Edit/$', 'edit_issue'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<issue_id>[-\w\./\s]+)/Delete/$', 'delete_issue'),
        (r'(?P<project_number>[-\w\./\s]+)/Add/$', 'add_issue'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<issue_id>[-\w\./\s]+)/$', 'view_issue'),
        (r'(?P<project_number>[-\w\./\s]+)/$', 'view_issues'),
)

