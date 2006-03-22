import ez_setup # From http://peak.telecommunity.com/DevCenter/setuptools
ez_setup.use_setuptools()

from setuptools import setup, find_packages

#find_packages(),

setup(
    name = "WorkStyle",
    version = "0.2.1",
    url = 'http://trac.everes.net/workstyle/',
    download_url = 'http://sourceforge.jp/projects/workstyle/',
    author = 'everes.net',
    author_email = 'mtsuyuki at gmail.com',
    description = 'Getting Things Done TODO Management Web Application',
    license = 'BSD',
    packages = ['WorkStyle', 'WorkStyle.workstyle',
                'WorkStyle.workstyle.models', 'WorkStyle.workstyle.templatetags'],
    package_data = {
        '': ['LICENSE_django',
             'LICENSE_djangofcgi',
             'LICENSE_workstyle_mockup',
             'LICENSE_workstyle',
             'README'],
        '3party-script': ['*.py'],
        'WorkStyle': ['locale/en/LC_MESSAGES/*',
                      'locale/ja/LC_MESSAGES/*'],
        'WorkStyle.workstyle': ['templates/workstyle/*.html',
                                     'media/resources/*.js',
                                     'media/resources/skin/default/*.css',
                                     'media/resources/skin/default/image/*.png',
                                     'media/resources/skin/default/image/icon/*.png'],
    },
    zip_safe = False,
)
