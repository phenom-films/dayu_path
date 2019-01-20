from setuptools import setup

setup(
        name='dayu_path',
        version='0.4.1',
        packages=['dayu_path'],
        url='https://github.com/phenom-films/dayu_path',
        license='MIT',
        author='andyguo',
        author_email='andyguo@phenom-films.com',
        description='a python path lib optimized for Movie industry. Support scan for sequence files, extract frame count and many other useful functions.',
        long_description=open('README.rst').read(),
        classifiers=[
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Programming Language :: Python :: Implementation',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
        ],
)
