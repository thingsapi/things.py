"""Tests for resolving the Things database path."""

import os
from unittest import mock

from things import database


def test_explicit_thingsdb_bypasses_directory_discovery():
    configured_path = "/tmp/Things Database.thingsdatabase/main.sqlite"

    with mock.patch.dict(os.environ, {"THINGSDB": configured_path}):
        with mock.patch.object(database.glob, "iglob") as discovery:
            result = database.resolve_default_filepath()

    assert result == configured_path
    discovery.assert_not_called()


def test_database_discovery_is_used_without_thingsdb():
    discovered_path = "/tmp/ThingsData-test/Things Database.thingsdatabase/main.sqlite"

    with mock.patch.dict(os.environ, {}, clear=True):
        with mock.patch.object(
            database.glob, "iglob", return_value=iter([discovered_path])
        ) as discovery:
            result = database.resolve_default_filepath()

    assert result == discovered_path
    discovery.assert_called_once()
