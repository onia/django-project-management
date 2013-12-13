from django.contrib.sitemaps import Sitemap
from cms.models import PageContent, Page
from cms.cms_global_settings import *

class PageSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1

# Pages
    def items(self):
        if LANGUAGE_REDIRECT:
            return PageContent.objects.filter(page__in=[page.id for page in Page.objects.published()])
        else:
            return Page.objects.published()
    
    def lastmod(self, obj):
        return obj.modified
        return obj.pagecontent_set.order_by('-modified')[0].modified

