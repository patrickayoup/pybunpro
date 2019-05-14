import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


setup(
    name='pybunpro',
    version='1.0.0',
    author='Patrick Ayoup',
    author_email='patrick.ayoup@gmail.com',
    description='REST client for Bunpro',
    license='MIT',
    keywords='rest client japanese grammar',
    packages=['pybunpro'],
    install_requires=['requests',
                      'marshmallow',
                      'Click'],
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ]
)
