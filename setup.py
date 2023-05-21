"""A simple Python 3 library to read your Things app data."""

import os

from setuptools import find_packages, setup  # type: ignore


def package_files(directory):
    """Automatically add data resources."""
    paths = []
    # pylint: disable=unused-variable
    for path, _directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append((directory, [os.path.join(path, filename)]))
    return paths


APP = [""]
AUTHOR = "Alexander Willner, Michael B."
AUTHOR_MAIL = "alex@willner.ws"
DESCRIPTON = "A simple Python 3 library to read your Things app data."
URL = "https://github.com/thingsapi/things.py"
DATA_FILES = package_files("")
OPTIONS = {
    "argv_emulation": False,
}

with open("README.md", "r", encoding="utf-8") as fh:
    LONG_DESRIPTION = fh.read()

setup(
    app=APP,
    author=AUTHOR,
    author_email=AUTHOR_MAIL,
    name="things.py",
    description=DESCRIPTON,
    long_description=LONG_DESRIPTION,
    long_description_content_type="text/markdown",
    url=URL,
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: MacOS :: MacOS X",
        "Natural Language :: English",
    ],
    python_requires=">=3.7",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
