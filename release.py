#!/usr/bin/env python

import os
import sys
import subprocess

from setuptools.sandbox import run_setup

from git import Repo

project_root = os.path.dirname(os.path.abspath(__file__))
version_path = os.path.join(project_root, '.VERSION')
setup_path = os.path.join(project_root, 'setup.py')


os.chdir(project_root)
print(f'Changed working directory to project root: {project_root}')

with open(version_path) as f:
    version = f.read().strip()

repo = Repo(project_root)

if version in repo.tags:
    print(f'Tag {version} already used')
    sys.exit(1)

repo.create_tag(version)
print(f'Tag {version} created')

repo.remote.origin.push(version)
print(f'Tag {version} pushed')

run_setup(setup_path, ['sdist', 'bdist_wheel'])
print(f'Artifacts for {version} created')

subprocess.check_call(['python', '-m', 'twine', 'upload', 'dist/*'])
print(f'Uploaded {version} to pypi')
