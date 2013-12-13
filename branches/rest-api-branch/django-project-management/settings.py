# Django settings for dj_projects project.
import os
import logging

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = '/tmp/dpm.sql'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/London'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_DIR + '/new_site_media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '#dix&nn&*-k=4fhqh58+%^5nwecjh-n*m44uon65x)68qujy_x'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
	PROJECT_DIR + '/new_templates/',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.humanize',
    'django.contrib.sites',
	'projects',
	'lessons',
	'deliverables',
	'risks',
	'wbs',
	'change_management',
	'files',
	'issues',
	'cms',
	'tinymce',
	'filebrowser',
	'wip',
	'rota',
	'sorl.thumbnail',
    'api',
)

STATIC_DOC_ROOT = PROJECT_DIR + '/new_site_media/'

AUTHENTICATION_BACKENDS = (
	'django.contrib.auth.backends.ModelBackend',
)

CORE_PROJECT_MANAGERS = ['CORE_PROJECT_MANAGERS']

AUTH_PROFILE_MODEL = 'projects.UserProfile'
DATE_FORMAT = "D d M Y"

CMS_DISPLAY_ROOT = True
CMS_DEFAULT_TEMPLATE = 'documentation/base.html'
CMS_REQUIRE_LOGIN = True
CMS_LANGUAGE_REDIRECT = True
CMS_USE_TINYMCE = True

SERIALIZATION_MODULES = {
    'json': 'wadofstuff.django.serializers.json'
}

LOGIN_URL = '/accounts/login'

def get_debug_settings(log_name):
    log = logging.getLogger(log_name)
    if DEBUG:
        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler()
        f = logging.Formatter("%(levelname)s %(asctime)s module=%(module)s fn=%(funcName)s() line=%(lineno)d msg=%(message)s")
        h.setFormatter(f)
        log.addHandler(h)
    else:
        log.setLevel(logging.NOTSET)
    return log
