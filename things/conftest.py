"""Helper module to test the Things API documentation."""

import pytest
import things


@pytest.fixture(autouse=True)
def add_imports(doctest_namespace):  # noqa
    """Import default modules."""
    doctest_namespace["things"] = things
