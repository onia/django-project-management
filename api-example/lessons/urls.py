from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('lessons.views',
        (r'(?P<project_number>[-\w\./\s]+)/(?P<lesson_id>[-\w\./\s]+)/Edit/$', 'edit_lesson'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<lesson_id>[-\w\./\s]+)/Delete/$', 'delete_lesson'),
        (r'(?P<project_number>[-\w\./\s]+)/Add/$', 'add_lesson'),
        (r'(?P<project_number>[-\w\./\s]+)/(?P<lesson_id>[-\w\./\s]+)/$', 'view_lesson'),
        (r'(?P<project_number>[-\w\./\s]+)/$', 'view_lessons'),
)

