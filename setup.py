from setuptools import setup

setup(
    name="Stormfront",
    options={
        "build_apps": {
            # Build asteroids.exe as a GUI application
            "gui_apps": {
                "Stormfront": "src/main.py",
            },
            # Set up output logging, important for GUI apps!
            "log_filename": "$USER_APPDATA/Stormfront/output.log",
            "log_append": False,
            # Specify which files are included with the distribution
            "include_patterns": [
                "**/*.png",
            ],
            "exclude_patterns": [
                "src/test/*",
            ],
            # Include the OpenGL renderer
            "plugins": [
                "pandagl",
            ],
            # Specify the platforms to target
            "platforms": [
                "win_amd64",
                "macosx_10_9_x86_64",
                "manylinux2014_x86_64",
            ],
        }
    },
)
