'''
#!/usr/bin/env python

from distutils.core import setup

setup(name='TDA Tools',
      version='0.1',
      description='Tools for topological data analysis',
      author='',
      author_email='',
      url='',
      packages=['.'],
     )

'''

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TDA Tools", # Replace with your own username
    version="0.0.1",
    author="",
    author_email="",
    description="Tools for topological data analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
