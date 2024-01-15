import pathlib
import sys
from typing import List


class Dependency:
    def __init__(self, dep: str, rel: str, version: str):
        self.dep = dep
        self.rel = rel
        self.version = version

    def __str__(self) -> str:
        return self.dep + self.rel + self.version


def readDeps(file: pathlib.Path) -> List[Dependency]:
    deps = []

    with file.open("r", encoding="utf-8") as f:
        for line in f.readlines():
            line = line.strip()
            if line == "":
                continue

            parts = []
            separator = ""

            if "==" in line:
                separator = "=="
            elif ">=" in line:
                separator = ">="
            elif "@" in line:
                separator = "@"
            else:
                raise ValueError("Could not find expected separator in " + line)

            parts = line.split(separator)

            deps.append(Dependency(parts[0], separator, parts[1]))

    return deps


def printDeps(deps: List[Dependency]) -> List[str]:
    depStrs = []

    for dep in deps:
        depStrs.append(str(dep))

    return depStrs


def run() -> None:
    args = sys.argv[1:]
    if len(args) != 2:
        raise SystemExit("Must provide a file to update and a lock file")

    reqFileName = args[0]
    lockFileName = args[1]

    filePath = pathlib.Path(__file__).absolute()
    rootPath = filePath.parents[2]

    lockDeps = readDeps(rootPath.joinpath(lockFileName))
    reqDeps = readDeps(rootPath.joinpath(reqFileName))

    for dep in reqDeps:
        if dep.rel != ">=":
            continue

        for lock in lockDeps:
            if dep.dep != lock.dep:
                continue

            dep.version = lock.version

    reqDeps.sort(key=lambda dep: dep.dep)

    with rootPath.joinpath(reqFileName).open("w", encoding="utf-8") as f:
        for result in printDeps(reqDeps):
            f.write(result + "\n")


if __name__ == "__main__":
    run()
