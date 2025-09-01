"""Helper module to test the Things API documentation."""

import pytest

import things


@pytest.fixture(autouse=True)
def add_imports(doctest_namespace):  # noqa
    """Import default modules."""
    doctest_namespace["things"] = things

@pytest.fixture
def patch_today(mocker):
    mock = mocker.patch("things.database.date_today")
    mock.return_value = '2025-09-01'