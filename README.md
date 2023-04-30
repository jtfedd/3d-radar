# 3D Radar

This is a project to build a 3d rendering program which can visualize full 3d nexrad level 2 data scans.

## Requirements

### Python

This project is written in [Python](https://www.python.org/). It is currently developed with Python 3.10; your milage may vary with other versions.

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

Once you have your virtual environment activated, run the following command to fetch the project dependencies:
```
pip install -r requirements.txt
```

### Testing

This project uses [unittest](https://docs.python.org/3/library/unittest.html) for unit testing.

To run all tests in the project:
```
python -m unittest
```

To run individual test files:
```
python -m unittest <path/to/test/file.py>
```

### Formatting

The code in this project is formatted with [black](https://pypi.org/project/black/#description).

To format all files:
```
python -m black .
```

To format individual files:
```
python -m black <path/to/file.py>
```

