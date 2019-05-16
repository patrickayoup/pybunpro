import os
from setuptools import setup


def read(file_name):
    return open(os.path.join(os.path.dirname(__file__), file_name)).read()


# TODO: Include a release command which will validate
# the version file against tags before tagging
setup(
    name='pybunpro',
    version=read('.VERSION'),
    author='Patrick Ayoup',
    author_email='patrick.ayoup@gmail.com',
    url='http://patrickayoup.github.io/pybunpro',
    description='REST client for Bunpro',
    license='MIT',
    keywords='rest client japanese grammar',
    packages=['pybunpro'],
    entry_points={
        'console_scripts': ['pybunpro=pybunpro.__main__:cli']
    },
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
