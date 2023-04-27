# 3D Radar

This is a project to build a 3d rendering program which can visualize full 3d nexrad level 2 data scans.

## Requirements

### Python

This project is written in [Python](https://www.python.org/). It is currently developed with Python 3.10; your milage may vary with other version.

### Set up a virtual environment

It is recommended that you set up a python virtual environment before fetching dependencies. This keeps project dependencies from conflicting with each other if you are developing on multiple environments. However, you can also fetch dependencies without setting up a virtual environment if you wish to install the dependencies globally for your system. For more information on python virual environments, [this](https://realpython.com/python-virtual-environments-a-primer/) is a helpful guide.

Create a virtual environment:
```
python -m venv .venv
```
Activate the virual environment:
```
Windows:
venv/Scripts/activate
Linux/Mac
source venv/bin/activate
```
Deactivate the virtual environment:
```
deactivate
```
### Dependencies

Once you have your virtual environment activated, run the following command to fetch the project dependencies:
```
pip install -r requirements.txt
```