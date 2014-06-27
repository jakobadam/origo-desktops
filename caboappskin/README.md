#

Check out repo:
```
hg clone https://hg.cabo.dk/django-caboappskin caboappskin
```

Install deps:
```
apt-get install nodejs nodejs-legacy npm
pip install djangobower
```

Update django settings file. In settings.py:
```python

INSTALLED_APPS = (
    'djangobower',
    'caboappskin'
)

BOWER_INSTALLED_APPS = (
    'jquery#1.9',
    'jquery-ui#1.10',
    'bootstrap#3.1.0',
    'Flat-UI#2.1.3',
    'html5shiv',
    'respond'
)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'djangobower.finders.BowerFinder',
    )

BOWER_COMPONENTS_ROOT = os.path.join(BASE_DIR, 'components')
```


