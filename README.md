# aienvs
Repository for Influence project environments

## Requirements
* Ubuntu Linux
* Built version of SUMO (download from sourceforge.net/projects/sumo).
* Add the sumo/tools directory to your pythonpath.
* Set the SUMO_HOME environment variable to point to your sumo directory

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

## Setting up a venv
Venv preparation usually goes like this
* Create venv (```cd aienvs``` and then ```python3 -m venv venv```)
* Start up venv with ```source venv/bin/activate```
* Install all dependencies with ```pip install```. The list of dependencies is in the setup.py file, check the "install-requires" field.



## Using from Eclipse
You can also use the Eclipse IDE to get better editing and debugging support.
Setup goes like this
* Follow the venv setup procedure as above (we assume you want to use a venv in PyDev, you can also use it without if you prefer).
* Install PyDev into Eclipse
* Add an interpreter 
 * Window/Preferences; go to PyDev/Interpreters/Python Interpreter
 * "Browse for python/pypy exe". Cancel the dialog (it does not work) and instead manually add the path to your python interpreter ```......./venv/bin/python```
 * Click ok.
* Set up the python path for Eclipse (it's not automatically recognising it as you would expect)
 * Right click on the aienvs project folder in the package explorer and select PyDev-PYTHONPATH.
 * In the Source Folders tab, add tha aienvs root as source folder
 * In the External Libraries tab, add ```..../sumo/tools``` (tools dir inside your sumo installation) as source folder. 
* In your debug/run settings, you may have to add an environment variable SUMO_HOME als pointing to ```...../sumo```.
