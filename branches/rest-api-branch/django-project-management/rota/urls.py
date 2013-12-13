from django.conf.urls.defaults import *
from django.contrib.auth.views import *

urlpatterns = patterns('rota.views',
        (r'^ViewAll/$', 'rota_homepage', { 'rota_url': '/Rota/RotaItems/' }),
        (r'^ViewMyTeam/$', 'rota_homepage', { 'rota_url': '/Rota/MyTeam/' }),
        (r'^ViewMyRota/$', 'rota_homepage', { 'rota_url': '/Rota/MyRota/' }),
        
        (r'RotaItems/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'view_rota', { 'pdf': False, 'scope': 'all' }),
        (r'MyTeam/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'view_rota', { 'pdf': False, 'scope': 'team' }),
        (r'MyRota/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'view_rota', { 'pdf': False, 'scope': 'user' }),

        (r'^RotaItems/$', 'view_rota', {'pdf': False, 'scope': 'all' }),
        (r'^MyTeam/$', 'view_rota', {'pdf': False, 'scope': 'team' }),
        (r'^MyRota/$', 'view_rota', {'pdf': False, 'scope': 'user' }),

        (r'^RotaActivities/$', 'view_rota_activities'),
#(r'^Rota/$', 'view_rota_items'),
        (r'^Users/$', 'view_users'),
        
        (r'GetRotaFor/(?P<user_id>\d{1,4})/(?P<date>(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01]))/$', 'get_rota_for_user'),
        (r'^Edit/$', 'edit_rota'),

)

