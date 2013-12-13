from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('deliverables.views',
        (r'(?P<project_number>[-\w\./\s]+)/Add/$', 'add_deliverable'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<deliverable_id>[-\w\./\s]+)/Edit/$', 'edit_deliverable'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<deliverable_id>[-\w\./\s]+)/Delete/$', 'delete_deliverable'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<deliverable_id>[-\w\./\s]+)/$', 'view_deliverable'),
        (r'(?P<project_number>[-\w\./\s]+)/$', 'view_deliverables'),
)

