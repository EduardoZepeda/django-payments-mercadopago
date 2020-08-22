#!/usr/bin/env python
from setuptools import setup


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
    version='0.1',
    url='https://github.com/EduardoZepeda/django-payments-mercadopago',
    download_url = 'https://github.com/EduardoZepeda/django-payments-mercadopago/archive/v0.1.tar.gz',
    packages=PACKAGES,
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
    keywords = ['django-payments', 'mercadopago'],
    zip_safe=False)
