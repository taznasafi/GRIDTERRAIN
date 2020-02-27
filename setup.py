try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': "This tool creates terrain standard deviation based for a given geographic border",
    'author': "Murtaza Nasafi",
    'author_email': "murtaza.nasafi@fcc.gov",
    'version': '0.1',
    'install_requires': ['nose', 'arcpy'],
    'packages': ['GRIDTERRAIN'],
    'scripts': [],
    'name': 'StdMaker'
}

setup(**config)
