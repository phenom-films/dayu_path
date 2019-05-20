"""Describe the distribution to distutils."""

# Import third-party modules
from setuptools import find_packages
from setuptools import setup

# Import local modules
import dayu_path

setup(
    name='dayu_path',
    package_dir={'': '.'},
    packages=find_packages('.'),
    url='https://github.com/phenom-films/dayu_path',
    license='MIT',
    author=dayu_path.__author__,
    version=dayu_path.__version__,
    author_email='andyguo@phenom-films.com',
    description=('a python path lib optimized for Movie industry. Support '
                 'scan for sequence files, extract frame count and many '
                 'other useful functions.'),
    long_description=open('README.rst').read(),
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest']
)
