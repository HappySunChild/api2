import setuptools

setup_info = {
	'name': 'api2',
	'version': '1.2.3',
	'author': 'HappySunChild',
	'description': 'A python library meant to make interfacing with the Roblox API simpler. Designed with work with python 3.9+',
	'url': 'https://github.com/HappySunChild/api2',
	'packages': setuptools.find_packages(),
	'python_requires': '>=3.9',
	'install_requires': [
		'requests>=2.25.1',
		'python-dateutil>=2.8.0'
	]
}

setuptools.setup(**setup_info)