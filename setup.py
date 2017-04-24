#!/usr/bin/env python

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='IOT_GD',
	  version='1.0.8',
	  description='IoT. You can read moacon modules (Modbus communication - cubloc.com) and mcp3208 - 8 channel 12Bit ADC from Rpi 3 and others.',
	  # long_description='long description',
	  long_description=long_description,
	  author='Sergio Sanchez, Ruben Morales',
	  license='Mozilla Public License Version 2.0',
	  classifiers=[
		# How mature is this project? Common values are
		#   3 - Alpha
		#   4 - Beta
		#   5 - Production/Stable
		'Development Status :: 4 - Beta',
		'Development Status :: 5 - Production/Stable',
		# Indicate who your project is intended for
		'Intended Audience :: Education',
		'Intended Audience :: Developers',
		'Topic :: System :: Hardware :: Hardware Drivers',

		# Pick your license as you wish (should match "license" above) 
		'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',

		# Specify the Python versions you support here. In particular, ensure
		# that you indicate whether you support Python 2, Python 3 or both.
		'Programming Language :: Python :: 2',
		'Programming Language :: Python :: 2.6',
		'Programming Language :: Python :: 2.7',
		# 'Programming Language :: Python :: 3',
		# 'Programming Language :: Python :: 3.2',
		# 'Programming Language :: Python :: 3.3',
		# 'Programming Language :: Python :: 3.4',
		'Operating System :: POSIX :: Linux',
		'Natural Language :: English',
	],
	  author_email='sergio.sanchezs@ingenieros.com',
	  keywords='IOT_GD moacon ADC modbus rs-485 spi Analog',
	  url='https://github.com/sergiosanchezs/IOT-GD',
	  # packages=['IOT_GD'],
	  # # package_dir={'IOT_GD':'/home/pi/IOT_GD'},
	  # package_dir={find_packages},
	  # package_data={ 'IOT_GD': ['IOT_GD/*.py'] },
	  # packages=['IOT_GD', 'IOT_GD.command', 'moacon', 'moacon.command'],
	  packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
	  package_data={ 'IOT_GD': ['moacon.py'] },
	  # packages=find_packages('moacon	','mcp3208'),
	  # packages={'IOT_GD'},
	  # install_requires=[''],
	 )