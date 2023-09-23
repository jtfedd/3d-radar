"""Verify Packages script verifies that all packages in src have an __init__.py file"""

import getopt
import pathlib
import sys
from typing import List

ignore = ["__pycache__", "cached_data"]

USAGE = """Verify that each python package has an __init__ file.
In the default usage mode the __init__ file will be created if it is not present.
In check mode the script will exit with an error if any expected file is not present.
OPTIONS
    -h, --help: Display this help page
    -c, --check: Run in check mode"""


def pathHasPythonChild(path: pathlib.Path) -> bool:
    for child in path.iterdir():
        if child.is_dir():
            if pathHasPythonChild(child):
                return True
        if child.is_file():
            if child.suffix == ".py":
                return True

    return False


def checkPath(path: pathlib.Path) -> List[pathlib.Path]:
    """Searches the path for missing __init__.py files

    Recursively scans the given path and any subdirectories for
    __init__.py files and returns the paths that are missing __init__.py
    """
    if path.is_file():
        return []

    if path.name in ignore:
        return []

    if not pathHasPythonChild(path):
        return []

    missingInitFiles = []

    initPath = path.joinpath("__init__.py")
    if not initPath.exists():
        missingInitFiles.append(initPath)

    for child in path.iterdir():
        if child.is_dir():
            missingInitFiles += checkPath(child)

    return missingInitFiles


def collectMissingInitFiles() -> List[pathlib.Path]:
    """Searches for missing __init__.py files

    Starts at the current file and moves up to the repo root.
    Scans lib and test directories, and merges the results.
    """

    filePath = pathlib.Path(__file__).absolute()
    srcPath = filePath.parents[2].joinpath("src")

    libPath = srcPath.joinpath("lib")
    testPath = srcPath.joinpath("test")

    missingInitFiles = []
    missingInitFiles += checkPath(libPath)
    missingInitFiles += checkPath(testPath)
    return missingInitFiles


def parseArgs() -> bool:
    """Parses the command line arguments and returns whether to run in check mode"""

    options, arguments = getopt.getopt(
        sys.argv[1:],
        "hc",
        ["help", "check"],
    )
    check = False
    for option, _ in options:
        if option in ("-h", "--help"):
            print(USAGE)
            sys.exit()
        if option in ("-c", "--check"):
            check = True
    if len(arguments) > 2:
        raise SystemExit(USAGE)
    return check


def run() -> None:
    """Runs the package checker"""

    check = parseArgs()
    files = collectMissingInitFiles()
    for file in files:
        print(file)

    plural = "s" if len(files) != 1 else ""
    print("Found " + str(len(files)) + " package" + plural + " missing __init__.py")

    if check:
        if len(files) > 0:
            sys.exit(1)
        sys.exit(0)

    for file in files:
        file.touch()


if __name__ == "__main__":
    run()
