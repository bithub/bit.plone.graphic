from setuptools import setup, find_packages
import os

version = '0.7.0'

setup(name='bit.plone.graphic',
      version=version,
      description="Annotated graphics",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),

      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Ryan Northey',
      author_email='ryan@3ca.org.uk',
      url='',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['bit', 'bit.plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'plone.namedfile',
          'plone.formwidget.namedfile',
          'z3c.blobfile',
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
