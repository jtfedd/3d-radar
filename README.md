# 3D Radar Viewer

This is a project to build a 3d rendering program which can visualize full 3d nexrad level 2 data scans.

## Requirements

### Python

This project requires [Python 3.12](https://www.python.org/).

### Set up a virtual environment

For more information on python virual environments, [this](https://realpython.com/python-virtual-environments-a-primer/) is a helpful guide.

Create a virtual environment:
```
python -m venv .venv
```
Activate the virual environment:
```
Windows:
.venv/Scripts/activate
Linux/Mac
source .venv/bin/activate
```
Deactivate the virtual environment:
```
deactivate
```
### Dependencies

Dependencies for the project are managed using `pip`.

To install build dependencies:
```
make install
```

To install build and development dependencies:
```
make install-dev
```

To upgrade all dependencies:
```
make upgrade
```

### Running

Once dependencies have been installed, the program can be run:
```
make run
```

Several cache and config files may be saved when the program is run. To remove them, run the program and find the option to "Clear All Data and Exit" under Settings. The cache and config directory paths can also be found in the startup logs.

### Testing

This project uses [unittest](https://docs.python.org/3/library/unittest.html) for unit testing.

To run all tests in the project:
```
make test
```

To run individual test files:
```
cd src
python -m unittest <path/to/test/file.py>
```

### Formatting

The code in this project is formatted with [black](https://pypi.org/project/black/#description).

To format all code:
```
make format
```
