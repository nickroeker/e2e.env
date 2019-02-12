"""Setup file for e2e.env."""

from os import path
from setuptools import find_namespace_packages
from setuptools import setup

cwd = path.abspath(path.dirname(__file__))
with open(path.join(cwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

version = '0.1.0'

name = 'e2e.env'
description = "Easily model and convert environment variables you care about."
long_description_content_type = 'text/markdown'
url = 'https://github.com/nickroeker/e2e.env'
author = "Nic Kroeker"
licenze = "Apache 2.0"
packages = find_namespace_packages(include=['e2e.*'])

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Software Development :: Testing',
    'Topic :: Software Development :: Testing :: Acceptance',
]

install_requires = []  # type: ignore
extras_require = {
    'dev': [
        'tox',
        'pytest',
    ],
}

setup(
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type=long_description_content_type,
    url=url,
    author=author,
    license=licenze,
    packages=packages,
    classifiers=classifiers,
    install_requires=install_requires,
    extras_require=extras_require,
)
