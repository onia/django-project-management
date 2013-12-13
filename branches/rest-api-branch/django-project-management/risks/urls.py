from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('risks.views',
        (r'GetRiskNumber/$', 'get_risk_number'),
        (r'(?P<project_number>[-\w\./\s]+)/Add/$', 'add_risk'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<risk_id>[-\w\./\s]+)/Edit/$', 'edit_risk'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<risk_id>[-\w\./\s]+)/Delete/$', 'delete_risk'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<risk_id>[-\w\./\s]+)/$', 'view_risk'),
        (r'(?P<project_number>[-\w\./\s]+)/$', 'view_risks'),
)

