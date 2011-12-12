#!/usr/bin/env python


from distutils.core import setup

setup(name='Server Manager',
      version='1.0',
      description='Screen based server manager',
      author='Cheuveulu',
      author_email='cheuveulu@team-elite.fr',
      url='http://team-elite.fr/',
      packages=['servermanager'],
      scripts=['servermanager/bin/servermanager']
     )

