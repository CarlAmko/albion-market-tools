from setuptools import setup

setup(
	name='Albion Market Tools',
	version='0.1',
	description='Market Tools for Albion Online',
	author='Carl Amko',
	author_email='carl@carlamko.me',
	url='https://github.com/Okma/albion-market-tools',
	install_requires=[
		'requests>=2.26.0',
		'redis>=4.1.0'
	]
)
