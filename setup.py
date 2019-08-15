from setuptools import setup, find_packages
import sys, os.path

setup(name='aienvs',
    version='0.1',
    description='environments for Influence project.',
    url='https://github.com/INFLUENCEorg/aienvs',
    author='Influence TEAM',
    author_email='author@example.com',
    license='Example',
    packages=['aienvs', 'aienvs/Sumo', 'aienvs/FactoryFloor', 'aienvs/listener'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[ 'aiagents', 'gym', 'mock', 'pyyaml', 'numpy', 'networkx']

)
