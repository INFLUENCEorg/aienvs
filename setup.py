from setuptools import setup, find_packages
import sys, os.path
from glob import glob

setup(name='aienvs',
    version='0.1',
    description='environments for Influence project.',
    url='https://github.com/INFLUENCEorg/aienvs',
    author='Influence TEAM',
    author_email='author@example.com',
    license='Example',
    # include_package_data=True,
    # package_dir={'scenarios':'scenarios'},
    package_data={'':['*.xml', '*.sumocfg', '*.txt']},
    packages=[ 'aienvs', 'aienvs/gym', 'aienvs/runners' ,
              'aienvs/loggers', 'scenarios',
              'aienvs/Sumo', 'aienvs/FactoryFloor', 'aienvs/listener',
              'aienvs/GroupingRobots', 'aienvs/Warehouse'
    ],
    data_files=[
                ('scenarios', glob('scenarios/**/*.*', recursive=True))
    ],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[  'gym', 'pyyaml', 'numpy', 'networkx', 'gym[atari]', 'matplotlib']

)
