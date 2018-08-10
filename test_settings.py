SECRET_KEY = "lorem ipsum"

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',

    'tango_shared',
    'easy_thumbnails',
    'tango_comments',
    'tests.custom_comments',
    'tests.testapp'
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

SITE_ID = 1

ROOT_URLCONF = 'tango_comments.urls'

AUTH_USER_MODEL = 'auth.User'

#stripped down middleware
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]

# TO-DO: Pull from tango_shared
PROFANITIES_LIST = []
COMMENTS_ALLOW_PROFANITIES = True