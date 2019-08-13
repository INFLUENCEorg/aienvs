# aienvs
Repository for Influence project environments

### Build the library ###
To build the library, you need to have version 40.6.2 or later of setuptools, plus wheel. To ensure, run
```
pip3 install --upgrade setuptools
pip3 install wheel
```
With that, you can build the library build using
```
./build.sh
(or sudo ./build.sh depending on your user privileges)

WARNING: It may be that some python libraries need to be installed manually (via pip3 install..),
not all dependencies are listed in setup.py yet..
