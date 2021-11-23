#!/usr/bin/env python
from setuptools import setup, find_packages
import os
import sys


# 'setup.py publish' shortcut.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist bdist_wheel')
    os.system('twine upload dist/*')
    sys.exit()

description = 'Financial data of a company.'

with open('README.md', 'r') as f:
    long_description = f.read()

install_requires = [
    '',
]

project_urls = {
  'Source': 'https://github.com/choi-jiwoo/financialdatapy',
}

setup(
    name='financialdatapy',
    version='0.1.0',
    author='Choi Jiwoo',
    author_email='cho2.jiwoo@gmail.com',
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    keywords=['python', 'stock', 'finance'],
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    project_urls=project_urls,
)
