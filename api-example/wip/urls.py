from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('wip.views',
        (r'(?P<wip_report>[-\w\./\s]+)/AddEngineeringDay/(?P<work_item_id>[-\w\./\s]+)/$', 'add_wip_engineering_day'),
        (r'Download/(?P<wip_report>[-\w\./\s]+)/$', 'download_wip_report'),
        (r'DownloadArchive/(?P<wip_archive>[-\w\./\s]+)/$', 'download_wip_archive'),
        (r'MyWIP/$', 'view_my_wip'),
        (r'(?P<wip_report>[-\w\./\s]+)/Archives/$', 'get_archives'),
        (r'(?P<wip_report>[-\w\./\s]+)/EngineeringDayResources/(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})//$', 'get_resources_for_engineering_day', {'day_type': None}),
        (r'(?P<wip_report>[-\w\./\s]+)/EngineeringDayResources/(?P<year>\d{4})-(?P<month>\d{1,2})-(?P<day>\d{1,2})/(?P<day_type>\d{1})/$', 'get_resources_for_engineering_day'),
        (r'(?P<wip_report>[-\w\./\s]+)/WIPItem/Add/$', 'add_work_item'),
        (r'(?P<wip_report>[-\w\./\s]+)/Heading/Add/$', 'add_heading'),
        (r'(?P<wip_report>[-\w\./\s]+)/Headings/$', 'view_headings'),
        (r'(?P<wip_report>[-\w\./\s]+)/xhr/assignees/$', 'xhr_get_assignees'),
        (r'(?P<wip_report>[-\w\./\s]+)/(?P<work_item_id>[-\w\./\s]+)/Complete/$', 'complete_work_item'),
        (r'(?P<wip_report>[-\w\./\s]+)/(?P<work_item_id>[-\w\./\s]+)/Update/$', 'update_work_item'),
        (r'(?P<wip_report>[-\w\./\s]+)/Objectives/$', 'view_wip_report', { 'objectives': True }),
        (r'(?P<wip_report>[-\w\./\s]+)/(?P<work_item_id>[-\w\./\s]+)/$', 'view_work_item'),
        (r'(?P<wip_report>[-\w\./\s]+)/$', 'view_wip_report'),
        (r'', 'all_wip_reports'),
)

