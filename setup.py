#!/usr/bin/env python
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import os
import sys

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

REQUIREMENTS = [
    'mercadopago>=0.3.5',
    'Django>=2.0.0',
    'django-payments>=0.12.3',
]

setup_requirements = ['setuptools_scm']

test_requirements = ['pytest', 'pytest-django']

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test_settings')


class PyTest(TestCommand):
    user_options = [
        ('pytest-args=', 'a', "Arguments to pass to py.test")]
    test_args = []

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    author="Eduardo Zepeda",
    author_email='eduardozepeda@coffeebytes.dev',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',

    ],
    description="A mercadopago payment gateway backend for django-payments.",
    install_requires=REQUIREMENTS,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['django-payments', 'mercadopago', 'django'],
    name='django-payments-mercadopago',
    packages=find_packages(
        include=['payments_mercadopago', 'payments_mercadopago.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/EduardoZepeda/django-payments-mercadopago',
    download_url='https://github.com/EduardoZepeda/django-payments-mercadopago/archive/0.4.0.tar.gz',
    version='0.4.1',
    cmdclass={
        'test': PyTest},
    zip_safe=False,
)
