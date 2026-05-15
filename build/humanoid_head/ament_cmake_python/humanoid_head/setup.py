from setuptools import find_packages
from setuptools import setup

setup(
    name='humanoid_head',
    version='0.1.0',
    packages=find_packages(
        include=('humanoid_head', 'humanoid_head.*')),
)
