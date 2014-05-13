from setuptools import setup, find_packages
import sys, os

version = '0.1'

base_requires = [
    'Chameleon',
    'cromlech.browser',
    'cromlech.configuration',
    'cromlech.dawnlight >= 0.7',
    'cromlech.security',
    'cromlech.webob',
    'dolmen.forms.base',
    'dolmen.forms.crud',
    'dolmen.forms.ztk',
    'dolmen.layout',
    'dolmen.location',
    'dolmen.menu',
    'dolmen.message',
    'dolmen.request',
    'dolmen.tales',
    'dolmen.template',
    'dolmen.view[security]',
    'dolmen.viewlet',
    'grokcore.component',
    'grokcore.security',
    'martian',
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
    'dolmen.content',
    'cromlech.zodb',
    ]

sql_requires = [
    'SQLAlchemy',
    'cromlech.sqlalchemy',
    'dolmen.sqlcontainer',
    ]

mongo_requires = [
    'pymongo',
    ]

traject_requires = [
    'traject',
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
        },
    entry_points="""
      # -*- Entry points: -*-
      [chameleon.tales]
      provider = dolmen.tales:SlotExpr
      """,
      )
