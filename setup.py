#!/usr/bin/env python
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

PACKAGES = [
    'payments_mercadopago',
]

REQUIREMENTS = [
    'mercadopago>=0.3.5',
    'Django>=2.0.0',
    'django-payments>=0.12.3',
]

setup(
    name='django-payments-mercadopago',
    author='Eduardo Zepeda',
    author_email='eduardozepeda@coffeebytes.dev',
    description='A django-payments backend for the mercadopago payment gateway',
    version='v0.3',
    url='https://github.com/EduardoZepeda/django-payments-mercadopago',
    download_url = 'https://github.com/EduardoZepeda/django-payments-mercadopago/archive/v0.3.tar.gz',
    packages=PACKAGES,
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules'],
    install_requires=REQUIREMENTS,
    keywords = ['django-payments', 'mercadopago', 'django'],
    zip_safe=False)
