#!/bin/sh
pip3 install --upgrade setuptools
pip3 install wheel
python3 setup.py sdist bdist_wheel
pip3 install dist/aienvs-0.1.tar.gz
