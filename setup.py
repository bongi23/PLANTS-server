# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "1.0.0"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="P.L.A.N.T.S. 3rd party api",
    author_email="",
    url="",
    keywords=["Swagger", "P.L.A.N.T.S. 3rd party api"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/api.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    Provides functions to 3rd parties
    """
)

