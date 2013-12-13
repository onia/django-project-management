from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('projects.ext-views',
        (r'get_companies/$', 'get_companies'),
        (r'(?P<project_number>[-\w\./\s]+)/get_users/$', 'get_users'),
        (r'(?P<project_number>[-\w\./\s]+)/get_skillset/$', 'get_skillset'),
        (r'(?P<project_number>[-\w\./\s]+)/edit_pid/$', 'edit_pid'),
        (r'(?P<project_number>[-\w\./\s]+)/get_team_managers/$', 'get_team_managers'),
        (r'(?P<project_number>[-\w\./\s]+)/get_non_team_managers/$', 'get_non_team_managers'),
)

