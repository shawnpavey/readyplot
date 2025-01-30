#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:34:59 2025
Custom plotter function which copies styles used by Shawn Pavey in Prism. Many
inputs are customizable, but defaults work well. This script contains two
functions: custom_plotter (full plotting + formating) and prism_reskin (only
reformats given figures).
@author: paveyboys
"""
from setuptools import setup, find_packages

setup(
    name="readyplot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'os',
        'seaborn',
        'scipy',
        'pathlib',
        'setuptools',  # Add any other dependencies your package needs
    ],
    description="A class plotting package with science publication-ready plots",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Shawn N. Pavey",
    author_email="shawn.pavey@yahoo.com",
    url="https://github.com/shawnpavey/readyplot",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)