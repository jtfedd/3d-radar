import pathlib
import subprocess


def convertModels(path: pathlib.Path) -> None:
    for child in path.iterdir():
        if child.is_dir():
            convertModels(child)
            continue

        if child.suffix == ".glb":
            print(child)
            subprocess.run(["gltf2bam", str(child)], check=True)


if __name__ == "__main__":
    filePath = pathlib.Path(__file__).absolute()
    srcPath = filePath.parents[2].joinpath("src")

    convertModels(srcPath)
