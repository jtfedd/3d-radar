# 3D Radar

This is a project to build a 3d rendering program which can visualize full 3d nexrad level 2 data scans.

## Requirements

### Python

This project is written in [Python](https://www.python.org/). It is currently developed with Python 3.11; your milage may vary with other versions.

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

To install all dependencies:
```
make install
```

To upgrade all dependencies:
```
make upgrade
```

Dependencies will also be automatically upgraded weekly by a [workflow](https://github.com/jtfedd/3d-radar/actions/workflows/upgrade_deps.yml).

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
