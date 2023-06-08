import getopt
import pathlib
import sys

ignore = ["__pycache__", "cached_data"]

USAGE = """Verify that each python package has an __init__ file.
In the default usage mode the __init__ file will be created if it is not present.
In check mode the script will exit with an error if any expected file is not present.
OPTIONS
    -h, --help: Display this help page
    -c, --check: Run in check mode"""


def checkPath(path: pathlib.Path):
    if path.is_file():
        return []

    if path.name in ignore:
        return []

    missingInitFiles = []

    initPath = path.joinpath("__init__.py")
    if not initPath.exists():
        missingInitFiles.append(initPath)

    for child in path.iterdir():
        if child.is_dir():
            missingInitFiles += checkPath(child)

    return missingInitFiles


def collectMissingInitFiles():
    filePath = pathlib.Path(__file__).absolute()
    srcPath = filePath.parents[2].joinpath("src")

    libPath = srcPath.joinpath("lib")
    testPath = srcPath.joinpath("test")

    missingInitFiles = []
    missingInitFiles += checkPath(libPath)
    missingInitFiles += checkPath(testPath)
    return missingInitFiles


def parseArgs():
    options, arguments = getopt.getopt(
        sys.argv[1:],
        "hc",
        ["help", "check"],
    )
    check = False
    for o, a in options:
        if o in ("-h", "--help"):
            print(USAGE)
            sys.exit()
        if o in ("-c", "--check"):
            check = True
    if len(arguments) > 2:
        raise SystemExit(USAGE)
    return check


def run():
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
