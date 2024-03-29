#!/usr/bin/env python

from distutils.core import setup
from LanConnect import VERSION

setup(
      name='LanConnect',
      version=".".join(str(x) for x in VERSION),
      description='Named Binary Tag Reader/Writer',
      author='Thomas Woolford et. al.',
      author_email='woolford.thomas@gmail.com',
      url='http://github.com/twoolie/NBT',
      license = open("LICENSE.txt").read(),
      long_description = open("README.txt").read(),
      packages=['LanConnect'],
     )
