#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import (
    find_packages,
    setup,
)

extras_require = {
    'linter': [
        'ruff==0.12.0',
        'isort==6.0.1',
        'importlib-metadata==8.7.0',
    ],
    'dev': [
        'PyInstaller==5.12.0',
        'pytest==8.4.1',
        'twine==6.1.0',
        'mock==5.2.0',
    ],
}

extras_require['dev'] = extras_require['linter'] + extras_require['dev']

setup(
    name='universal-cli',
    version='1.0',
    description='SKALE Manager Universal CLI',
    long_description_markdown_filename='README.md',
    author='SKALE Labs',
    author_email='support@skalelabs.com',
    url='https://github.com/skalenetwork/universal-cli',
    include_package_data=True,
    install_requires=['skale.py==7.3dev6', 'python-dotenv==1.1.0', 'click==8.2.1'],
    python_requires='>=3.11,<4',
    extras_require=extras_require,
    keywords='skale',
    packages=find_packages(exclude=['tests']),
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.11',
    ],
)
