#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from things3.things3 import Things3


class Things3Case(unittest.TestCase):
    """Class documentation goes here."""

    def setUp(self):
        self.things3 = Things3(database='tests/demo.sqlite3')
        self.things3.tag_mit = 'MIT'

    def test_today(self):
        """Test Today."""
        tasks = self.things3.get_today()
        self.assertEqual(4, len(tasks))
        titles = []
        for task in tasks:
            titles.append(task['title'])
        self.assertIn("Today MIT task without a project", titles)
        self.assertIn("Today items are shown here", titles)

    def test_inbox(self):
        """Test Inbox."""
        tasks = self.things3.get_inbox()
        self.assertEqual(3, len(tasks))
        titles = []
        for task in tasks:
            titles.append(task['title'])
        self.assertIn("Currently Things 3 tasks are supported", titles)
        self.assertIn("This is a demo setup", titles)
        self.assertIn("New tasks are shown here", titles)

    def test_upcoming(self):
        """Test Upcoming."""
        tasks = self.things3.get_upcoming()
        self.assertEqual(5, len(tasks))
        titles = []
        for task in tasks:
            titles.append(task['title'])
        self.assertIn("Waiting for this...", titles)

    def test_next(self):
        """Test Next."""
        tasks = self.things3.get_anytime()
        self.assertEqual(29, len(tasks))

    # def test_backlog(self):
    #     """Test Backlog."""
    #     tasks = self.things3.get_someday()
    #     self.assertEqual(1, len(tasks))

    def test_waiting(self):
        """Test Waiting."""
        tasks = self.things3.get_waiting()
        self.assertEqual(3, len(tasks))

    def test_mit(self):
        """Test MIT."""
        tasks = self.things3.get_mit()
        self.assertEqual(6, len(tasks))

    def test_completed(self):
        """Test completed tasks."""
        tasks = self.things3.get_completed()
        self.assertEqual(3, len(tasks))

    def test_cancelled(self):
        """Test cancelled tasks."""
        tasks = self.things3.get_cancelled()
        self.assertEqual(2, len(tasks))

    def test_trashed(self):
        """Test trashed tasks."""
        tasks = self.things3.get_trashed()
        self.assertEqual(10, len(tasks))

    def test_all(self):
        """Test all tasks."""
        tasks = self.things3.get_all()
        self.assertEqual(56, len(tasks))

    def test_due(self):
        """Test due tasks."""
        tasks = self.things3.get_due()
        self.assertEqual(1, len(tasks))

    def test_lint(self):
        """Test tasks that should be cleaned up."""
        tasks = self.things3.get_lint()
        self.assertEqual(4, len(tasks))

    def test_empty_projects(self):
        """Test projects that are emptÿ."""
        tasks = self.things3.get_empty_projects()
        self.assertEqual(2, len(tasks))

    def test_cleanup(self):
        """Test tasks that should be cleaned up."""
        tasks = self.things3.get_cleanup()
        self.assertEqual(7, len(tasks))

    def test_get_projects(self):
        """Test get projects."""
        projects = self.things3.get_projects()
        self.assertEqual(7, len(projects))

    def test_get_areas(self):
        """Test get areas."""
        areas = self.things3.get_areas()
        self.assertEqual(1, len(areas))

    def test_get_minutes_today(self):
        """Test get minutes today."""
        minutes = self.things3.get_minutes_today()
        self.assertEqual([{'minutes': 35}], minutes)

    def test_anonymize(self):
        """Test anonymized tasks."""
        tasks = self.things3.get_today()
        task = tasks.pop()
        self.things3.anonymize = True
        tasks = self.things3.get_today()
        self.assertNotEqual(tasks.pop(), task)


if __name__ == '__main__':
    unittest.main()
