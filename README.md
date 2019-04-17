# aienvs
Repository for Influence project environments

### Build the library ###
To build the library, you need to have version 40.6.2 or later of setuptools, plus wheel. To ensure, run
```
pip3 install --upgrade setuptools
pip3 install wheel
```
With that, you can run the library build using
```
#go to the directory containing setup.py
python3 setup.py sdist bdist_wheel
```

After this, the build is available in dist/sumoai..tar.gz 

