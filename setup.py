import glob
import io
import sys
import re
import os

from setuptools.command.test import test as TestCommand
from setuptools.command.install import install
from setuptools import setup, find_packages

description = "python micro tool"

setup(
    name='py_micro',
    version="1.0.2",
    author='yyl',
    author_email='1906600192@qq.com',
    # url='',
    description=description,
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "grpcio==1.27.2",
        "protobuf==3.10.0",
        "grpcio-tools==1.27.2",
        "python-consul==1.1.0",
    ],
)