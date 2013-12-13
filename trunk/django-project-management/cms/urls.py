from django.conf.urls.defaults import *
from cms.views import handler, search, get_tinymce_link_list

urlpatterns = patterns('',
    url(r'^search/', search, name='cms_search'),
    url(r'^cms/tiny_mce_links.js$', get_tinymce_link_list, name='cms_link_list'),
    url(r'^.*/$', handler),
    url(r'^$', handler, name='cms_root'),
)
