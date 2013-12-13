from django.conf.urls.defaults import *
from django.contrib.auth.views import *
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
	(r'^admin/filebrowser/', include('filebrowser.urls')),
    (r'^admin/(.*)', admin.site.root),
	
	(r'^$', 'projects.views.home_page'),
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	# Application URLS
	(r'^xhr/',      include('projects.xhr-urls')),
	(r'^Projects/',		include('projects.urls')),
	(r'^Risks/',		include('risks.urls')),
	(r'^Deliverables/',	include('deliverables.urls')),
	(r'^Issues/',		include('issues.urls')),
	(r'^Lessons/',		include('lessons.urls')),
	(r'^Files/',		include('files.urls')),
	(r'^WBS/',			include('wbs.urls')),
	(r'^WIP/',			include('wip.urls')),
	(r'^Rota/',			include('rota.urls')),
	(r'^admin/filebrowser/',		include('filebrowser.urls')),
	(r'^GetDoc/$', 'projects.views.get_doc'),

    # The REST API
    (r'^api/', include('api.urls')),

	# General
	(r'^accounts/login/', login, {'template_name': 'login.html'}),
    (r'^accounts/logout/', logout_then_login, {'login_url': '/'}),

	# TinyMCE
	(r'^tinymce/', include('tinymce.urls')),

	# CMS
    (r'', include('cms.urls')),
	
)
