"""Packaging shim (py2app): metadata lives in pyproject.toml."""

import os

import setuptools  # type: ignore # pylint: disable=import-error


def package_files(directory):
    """Automatically add data resources."""
    paths = []
    # pylint: disable=unused-variable
    for path, _directories, filenames in os.walk(directory):
        for filename in filenames:
            paths.append((directory, [os.path.join(path, filename)]))
    return paths


setuptools.setup(
    # name stays here (not only in pyproject.toml): py2app's finalize hook
    # reads it before pyproject metadata is merged; without it every
    # setup.py invocation fails with "no script, modules or dest_base specified".
    name="things.py",
    app=[""],
    packages=setuptools.find_packages(),
    data_files=package_files(""),
    options={"py2app": {"argv_emulation": False}},  # pyright: ignore[reportArgumentType]
    setup_requires=["py2app"],
)
