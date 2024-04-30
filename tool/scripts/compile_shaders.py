import pathlib
import sys
from typing import List

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


def compileShader(shader: pathlib.Path) -> None:
    shaderOut = getOutputPath().joinpath(shader.name)
    print("Compiling", shader, "to", shaderOut)

    with open(shader, "r", encoding="utf-8") as inputFile:
        with open(shaderOut, "w+", encoding="utf-8") as outputFile:
            for line in inputFile.readlines():
                if line.startswith("#include"):
                    outputFile.write("// ########## start " + line)
                    outputFile.write("\n")
                    includeFilename = line.strip().split(" ")[1]
                    includePath = getSrcPath().joinpath(includeFilename)
                    print("> Including", includePath)
                    with open(includePath, "r", encoding="utf-8") as includeFile:
                        for iline in includeFile.readlines():
                            outputFile.write(iline)

                    outputFile.write("\n")
                    outputFile.write("// ########## end " + line)
                else:
                    outputFile.write(line)


if __name__ == "__main__":
    removeCompiledShaders()
    shaders = collectShaders()

    for s in shaders:
        compileShader(s)
