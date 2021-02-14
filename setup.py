# OPBOT - operbot (setuo.py)
#
# This file is placed in the Public Domain.

from setuptools import setup

def readme():
    with open('README.rst') as file:
        return file.read()

setup(
    name='opbot',
    version='3',
    url='https://github.com/bthate/opbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="operbot",
    long_description=readme(),
    license='Public Domain',
    install_requires=["oplib", "feedparser"],
    packages=["opbot", "opm"],
    namespace_packages=["opbot", "opm"],
    scripts=["bin/op", "bin/opbot", "bin/opbotd", "bin/opctl"],
    zip_safe=False,
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
