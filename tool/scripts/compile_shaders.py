# pylint: disable=broad-exception-caught
# pylint: disable=broad-exception-raised

import pathlib
import sys
from enum import Enum
from typing import Dict, List, Set

SHADER_SRC = "src/shaders"
SHADER_OUT = "src/shaders/gen"


def getOutputPath() -> pathlib.Path:
    filePath = pathlib.Path(__file__).absolute()
    outPath = filePath.parents[2].joinpath(SHADER_OUT)

    return outPath


def getSrcPath() -> pathlib.Path:
    filePath = pathlib.Path(__file__).absolute()
    srcPath = filePath.parents[2].joinpath(SHADER_SRC)

    return srcPath


def removeCompiledShaders() -> None:
    for file in getOutputPath().iterdir():
        print("Removing", str(file))
        file.unlink()


def collectShaders() -> List[pathlib.Path]:
    shaderFiles = []

    for file in getSrcPath().iterdir():
        if file.is_dir():
            if file != getOutputPath():
                print("Found unexpected directory", str(file))
                sys.exit(1)
            else:
                continue

        if file.suffix != ".glsl":
            print("Found unexpected file", str(file))
            sys.exit(1)

        if len(file.suffixes) > 2 or (
            len(file.suffixes) > 1 and file.suffixes[0] != ".part"
        ):
            print("Malformed filename", str(file))
            sys.exit(1)

        if len(file.suffixes) == 1 and file.suffix == ".glsl":
            print("Found shader", str(file))
            shaderFiles.append(file)
        else:
            print("Found fragment", str(file))

    return shaderFiles


class MetaState(Enum):
    NONE = 1
    INPUTS = 2
    CONSTANTS = 3


class Compiler:
    def __init__(self, shader: pathlib.Path) -> None:
        self.includes: Set[str] = set()

        self.constants: Dict[str, str] = {}
        self.constantsOrder: List[str] = []

        self.inputs: Dict[str, str] = {}
        self.inputsOrder: List[str] = []

        self.shaderIn = shader
        self.shaderOut = getOutputPath().joinpath(shader.name)

    def compile(self) -> None:
        print("Compiling", self.shaderIn, "to", self.shaderOut)

        lines = self.readFile(self.shaderIn)

        lines = self.collectMeta(lines)
        lines = self.processIncludes(lines)
        lines = self.applyMeta(lines)

        with open(self.shaderOut, "w+", encoding="utf-8") as outputFile:
            outputFile.write("\n".join(lines))

    def readFile(self, file: pathlib.Path) -> List[str]:
        with open(file, "r", encoding="utf-8") as f:
            contents = f.read()

        return contents.split("\n")

    def addInput(self, line: str) -> None:
        parts = line.split(" ")
        t = parts[1]
        name = parts[2]

        if name in self.inputs and self.inputs[name] != t:
            raise Exception(
                "Conflicting types for " + name + ": " + self.inputs[name] + ", " + t
            )

        self.inputs[name] = t
        self.inputsOrder.append(name)

    def addConstant(self, line: str) -> None:
        parts = line.split(" ")
        name = parts[1]
        value = parts[2]

        if name in self.constants and self.constants[name] != value:
            raise Exception(
                "Conflicting values for "
                + name
                + ": "
                + self.constants[name]
                + ", "
                + value
            )

        self.constants[name] = value
        self.constantsOrder.append(name)

    def collectMeta(self, lines: List[str]) -> List[str]:
        outputLines: List[str] = []

        state = MetaState.NONE

        for line in lines:
            if line == "$end":
                state = MetaState.NONE
                continue

            if state == MetaState.INPUTS:
                self.addInput(line)
                continue

            if state == MetaState.CONSTANTS:
                self.addConstant(line)
                continue

            if line == "$begin inputs":
                state = MetaState.INPUTS
                continue

            if line == "$begin constants":
                state = MetaState.CONSTANTS
                continue

            outputLines.append(line)

        return outputLines

    def processIncludes(self, lines: List[str]) -> List[str]:
        outputLines: List[str] = []

        for line in lines:
            if line.startswith("#include"):
                includeFilename = line.strip().split(" ")[1]
                if includeFilename in self.includes:
                    print("> " + includeFilename + " already included")

                self.includes.add(includeFilename)
                includePath = getSrcPath().joinpath(includeFilename)
                print("> Including", includePath)

                lines = self.readFile(includePath)
                lines = self.collectMeta(lines)
                outputLines += lines
            else:
                outputLines.append(line)

        return outputLines

    def applyMeta(self, lines: List[str]) -> List[str]:
        outputLines: List[str] = []

        for line in lines:
            if line == "$inputs":
                for name in self.inputsOrder:
                    outputLines.append("uniform " + self.inputs[name] + " " + name)
            elif line == "$constants":
                for name in self.constantsOrder:
                    outputLines.append("#define " + name + " " + self.constants[name])
            else:
                outputLines.append(line)

        return outputLines


if __name__ == "__main__":
    try:
        removeCompiledShaders()
    except Exception as e:
        print("Failed to remove compiled shaders")
        print(e)
        sys.exit(1)

    try:
        shaders = collectShaders()
    except Exception as e:
        print("Failed to find shader files")
        print(e)
        sys.exit(1)

    for s in shaders:
        try:
            Compiler(s).compile()
        except Exception as e:
            print("Failed to compile", s)
            print(e)
            sys.exit(1)
