from setuptools import setup, find_packages
from os import path
here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zeal',
    version='0.0.1',

    description=('Ret shit.'),

    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/hypernormalisation/zeal',
    author='Swedge',
    author_email='sinope@tuta.io',
    classifiers=[
        'Development Status :: 4 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.9',
    ],

    keywords='ret',
    packages=find_packages(exclude=['docs', 'tests']),

    python_requires='>=3.9',
    install_requires=['matplotlib'],

    project_urls={
        'Bug Reports': 'https://github.com/hypernormalisation/zeal/issues',
        'Source': 'https://github.com/hypernormalisation/zeal',
    },
)
