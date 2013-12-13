###########################################################################
# Default CMS settings.  Do not change them. Edit your project's          # 
# settings.py file instead, prepending "CMS_" to the setting name.        # 
#                                                                         # 
# For example, add:                                                       # 
#                                                                         # 
# CMS_SITE_TITLE = "Your NEW site title"                                  # 
#                                                                         # 
# to your settings.py file to set the SITE_TITLE setting.                 # 
###########################################################################
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# The template that will be used for the website
DEFAULT_TEMPLATE = getattr(settings, 'CMS_DEFAULT_TEMPLATE', 'documentation/base.html')

# Site title for your template
SITE_TITLE = getattr(settings, 'CMS_SITE_TITLE', 'Your Site')
 
# Site name (for the file browser)
SITE_NAME = getattr(settings, 'CMS_SITE_NAME', 'yoursite')

# Whether content should be delivered on the root page (/)
DISPLAY_ROOT = getattr(settings, 'CMS_DISPLAY_ROOT', True)

# Whether we should use a language redirect (/ -> /de/) or cookies (not implemented!)
LANGUAGE_REDIRECT = getattr(settings, 'CMS_LANGUAGE_REDIRECT', True)

# Default language (e.g. de)
LANGUAGE_DEFAULT = getattr(settings, 'CMS_LANGUAGE_DEFAULT', 'en')

# overrides the language name when using cms_language_links template tag
LANGUAGE_NAME_OVERRIDE = getattr(settings, 'CMS_LANGUAGE_NAME_OVERRIDE', (
    ('de', 'Deutsche Version'),
    ('en', 'English version'),
))

# Whether there should be SEO fields for each page content
SEO_FIELDS = getattr(settings, 'CMS_SEO_FIELDS', False)

# Whether the whole page should be password protected
REQUIRE_LOGIN = getattr(settings, 'CMS_REQUIRE_LOGIN', False)

# Additional templatetags for the page content, e.g. ['yourapp.extras']
# will load yourapp/templatetags/extras.py (yourapp must be in INSTALLED_APPS)
TEMPLATETAGS = getattr(settings, 'CMS_TEMPLATETAGS', (
#    'project.app.module',
))

TEMPLATES = getattr(settings, 'CMS_TEMPLATES', (
#    ('project/custom_template.html', _('template name')),
))

PAGE_ADDONS = getattr(settings, 'CMS_PAGE_ADDONS', (
#    'project.app.models.File',
))

USE_TINYMCE = getattr(settings, 'CMS_USE_TINYMCE', False)

# Specify multiple content positions here.
# For example, you can have a separate page content for a sidebar.
POSITIONS = getattr(settings, 'CMS_POSITIONS', (
    ('', _('Default')),
#    ('left', _('Left column')),
#    ('right', _('Right column')),
))

# Find more options for the rst formatter at
# http://docutils.sourceforge.net/docs/user/config.html
RESTRUCTUREDTEXT_FILTER_SETTINGS = getattr(settings, 'CMS_RESTRUCTUREDTEXT_FILTER_SETTINGS', {
    'cloak_email_addresses': True,
    'file_insertion_enabled': False,
    'raw_enabled': False,
    'strip_comments': True,
})

# (deprecated) Override the global settings with site-specific settings.
try:
    from cms_settings import *
except ImportError:
    pass
