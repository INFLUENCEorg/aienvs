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

To use the scenarios in the project you need to export the environment variable
AIENVS_HOME to the root of your repository path
(e.g. by adding export AIENVS_HOME=/home/username/aienvs to your .bashrc and restarting the shell)
