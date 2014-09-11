from setuptools import setup, find_packages
import sys, os

version = '0.1'

base_requires = [
    'BeautifulSoup',
    'unidecode',
    'Chameleon',
    'cromlech.browser',
    'cromlech.configuration',
    'cromlech.dawnlight >= 0.7',
    'cromlech.security',
    'cromlech.webob',
    'cromlech.container',
    'cromlech.wsgistate',
    'dolmen.forms.base',
    'dolmen.forms.crud',
    'dolmen.forms.table',
    'dolmen.forms.viewlet',
    'dolmen.forms.ztk',
    'dolmen.layout',
    'dolmen.location',
    'dolmen.menu',
    'dolmen.container',
    'dolmen.message',
    'dolmen.request',
    'dolmen.tales',
    'dolmen.template[translate] >= 0.3.3',
    'dolmen.view[security]',
    'dolmen.viewlet',
    'GenericCache',
    'grokcore.component',
    'grokcore.security',
    'martian',
    'uvc.content',
    'uvc.design.canvas',
    'z3c.table',
    'zope.component',
    'zope.i18n',
    'zope.interface',
    'zope.security',
    ]

auth_requires = [
    'barrel',
    'cromlech.security',
    'cromlech.wsgistate',
    ]

zodb_requires = [
    'ZODB',
    'persistent',
    'cromlech.zodb',
    'dolmen.content',
    'dolmen.container',
    'zope.annotation',
    ]

sql_requires = [
    'transaction',
    'SQLAlchemy',
    'cromlech.sqlalchemy',
    'dolmen.sqlcontainer',
    'sqlalchemy_imageattach',
    'uvclight[traject]',
    ]

mongo_requires = [
    'pymongo',
    ]

traject_requires = [
    'traject',
    ]

websocket_requires = [
    'uwsgi',
    'gevent',
    'Flask-uWSGI-WebSocket',
    ]

tests_require = [
    'zope.location',
    'zope.event',
    'infrae.testbrowser',
    'pytest',
    'zope.configuration',
    'zope.schema',
    'zope.testing',
    'cromlech.browser[test]',
    ]


setup(
    name='uvclight',
    version=version,
    description="Layer on top of cromlech",
    long_description="""\
    """,
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Christian Klinger',
    author_email='ck@novareto.de',
    url='http://www.novareto.de',
    license='GPL',
    packages=find_packages('src'),
    package_dir = {'': 'src'},
    include_package_data=True,
    zip_safe=False,
    install_requires=base_requires,
    extras_require={
        'auth': auth_requires,
        'mongo': mongo_requires,
        'sql': sql_requires,
        'test': tests_require,
        'traject': traject_requires,
        'zodb': zodb_requires,
        'websocket': websocket_requires,
        },
    entry_points="""
      # -*- Entry points: -*-
      [chameleon.tales]
      provider = dolmen.tales:SlotExpr
      """,
      )
