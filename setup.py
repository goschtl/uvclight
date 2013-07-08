from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='uvclight',
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
      install_requires=[
          'cromlech.browser',
          'cromlech.dawnlight',
          'cromlech.security',
          'cromlech.sqlalchemy',
          'cromlech.webob',
          'cromlech.configuration',
          'zope.component',
          'zope.event',
          'zope.interface',
          'zope.location',
          'zope.security',
          'dolmen.layout',
          'dolmen.request',
          'dolmen.content',
          'dolmen.view',
          'dolmen.viewlet',
          'dolmen.tales',
          'dolmen.forms.base',
          'BeautifulSoup',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
