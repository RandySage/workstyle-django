# This Python file uses the following encoding: utf-8
# Django settings for WorkStyle project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'postgresql' # 'postgresql', 'mysql', 'sqlite3' or 'ado_mssql'.
DATABASE_NAME = 'workstyle92'    # Or path to database file if using sqlite3.
DATABASE_USER = 'workstyle92'    # Not used with sqlite3.
DATABASE_PASSWORD = 'workstyle92'# Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.


#WorkStyle origin settings
WORKSTYLE_BASE_DIR = '/open/svn/everes/WorkStyle/trunk/WorkStyle/WorkStyle'
WORKSTYLE_ROOT = '/WorkStyle'
WORKSTYLE_MEDIA_ROOT = WORKSTYLE_BASE_DIR + '/workstyle/media/resources'
WORKSTYLE_JUNK_DIR = 'junk'

TAG_TYPE_1  = 'TAG_TYPE_1'
TAG_TYPE_2  = 'TAG_TYPE_2'
TAG_TYPE_3  = 'TAG_TYPE_3'
TAG_TYPE_4  = 'TAG_TYPE_4'
TAG_TYPE_5  = 'TAG_TYPE_5'
TAG_TYPE_6  = 'TAG_TYPE_6'
TAG_TYPE_7  = 'TAG_TYPE_7'
TAG_TYPE_8  = 'TAG_TYPE_8'
TAG_TYPE_9  = 'TAG_TYPE_9'
TAG_TYPE_10 = 'TAG_TYPE_10'



# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Japan'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'ja'

SITE_ID = 1

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = WORKSTYLE_BASE_DIR + '/workstyle/media/resources'
#MEDIA_ROOT = 'E:\\everes.net\\WorkStyle\\resources'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = 'http://localhost:9000'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xw)k&_5jdvd@zc2urlvxcuv%*55-_scebpbk0n+72xh-5&l6pl'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.doc.XViewMiddleware",
)

ROOT_URLCONF = 'WorkStyle.urls'


TEMPLATE_DIRS = (
    #"E:\\everes.net\\WorkStyle\\WorkStyle\\apps\\workstyle\\template",
    WORKSTYLE_BASE_DIR + "/workstyle/templates",
    # Put strings here, like "/home/html/django_templates".
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'WorkStyle.workstyle',
    # 'django.contrib.admin', 
)
