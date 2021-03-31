#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest

import things


FILEPATH = dict(filepath="tests/main.sqlite")


class ThingsCase(unittest.TestCase):
    """Class documentation goes here."""

    def test_search(self):
        """Test search."""
        tasks = things.search("wrong_query", **FILEPATH)
        self.assertEqual(0, len(tasks))
        tasks = things.search("To-Do % Heading", **FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_inbox(self):
        """Test inbox."""
        tasks = things.inbox(**FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_upcoming(self):
        """Test upcoming."""
        tasks = things.upcoming(**FILEPATH)
        self.assertEqual(2, len(tasks))

    def test_deadlines(self):
        """Test deadlines."""
        tasks = things.deadlines(**FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_today(self):
        """Test today."""
        tasks = things.today(**FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_anytime(self):
        """Test antime."""
        tasks = things.anytime(**FILEPATH)
        self.assertEqual(8, len(tasks))

    def test_logbook(self):
        """Test logbook."""
        tasks = things.logbook(**FILEPATH)
        self.assertEqual(21, len(tasks))

    def test_canceled(self):
        """Test canceled."""
        tasks = things.canceled(**FILEPATH)
        self.assertEqual(11, len(tasks))

    def test_completed(self):
        """Test completed."""
        tasks = things.completed(**FILEPATH)
        self.assertEqual(10, len(tasks))

    def test_someday(self):
        """Test someday."""
        tasks = things.someday(**FILEPATH)
        self.assertEqual(1, len(tasks))

    def test_get(self):
        """Test get."""
        tasks = things.get("wrong_uuid", **FILEPATH)
        self.assertEqual(None, tasks)
        tasks = things.get("wrong_uuid", "NOT FOUND", **FILEPATH)
        self.assertEqual("NOT FOUND", tasks)
        tasks = things.get("Qt2AY87x2QDdowSn9HKTt1", **FILEPATH)
        self.assertEqual(4, len(tasks))

    def test_todos(self):
        """Test all tasks."""
        tasks = things.todos(start="Anytime", **FILEPATH)
        self.assertEqual(5, len(tasks))
        tasks = things.todos(start="Anytime", status="completed", **FILEPATH)
        self.assertEqual(6, len(tasks))
        tasks = things.todos(status="completed", **FILEPATH)
        self.assertEqual(10, len(tasks))
        tasks = things.todos(include_items=True, **FILEPATH)
        self.assertEqual(9, len(tasks))
        with self.assertRaises(ValueError):
            things.todos(status="wrong_value", **FILEPATH)
        tasks = things.tasks("A2oPvtt4dXoypeoLc8uYzY", **FILEPATH)
        self.assertEqual(13, len(tasks))

    def test_tags(self):
        """Test all tags."""
        tags = things.tags(**FILEPATH)
        self.assertEqual(5, len(tags))

    def test_projects(self):
        """Test all projects."""
        projects = things.projects(**FILEPATH)
        self.assertEqual(2, len(projects))

    def test_areas(self):
        """Test all test_areas."""
        test_areas = things.areas(**FILEPATH)
        self.assertEqual(1, len(test_areas))

    def test_database_version(self):
        """Test database version."""
        version = things.Database(**FILEPATH).get_version()
        self.assertEqual(18, version)


if __name__ == "__main__":
    unittest.main()
