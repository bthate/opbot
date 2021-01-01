# OPBOT - operbot (setuo.py)
#
# this file is placed in the public domain

from setuptools import setup

def readme():
    with open('README.rst') as file:
        return file.read()

setup(
    name='opbot',
    version='1',
    url='https://github.com/bthate/opbot',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="operbot",
    long_description=readme(),
    license='Public Domain',
    install_requires=["op"],
    packages=["opbot"],
    scripts=["bin/op", "bin/opbot", "bin/opcmd", "bin/opctl", "bin/opd", "bin/opudp"],
    zip_safe=True,
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
