#!/usr/bin/env python3

"""Module documentation goes here."""

import contextlib
import io
import os
import unittest

import things


TEST_DATABASE_FILEPATH = "tests/main.sqlite"

THINGSDB = things.database.ENVIRONMENT_VARIABLE_WITH_FILEPATH  # type: ignore


class ThingsCase(unittest.TestCase):  # noqa: V103 pylint: disable=R0904
    """Class documentation goes here."""

    def setUp(self):
        # Set environment variable to test database
        self.saved_filepath = os.getenv(THINGSDB)
        os.environ[THINGSDB] = TEST_DATABASE_FILEPATH

    def tearDown(self):
        # Restore environment variable to its previous value
        # or delete it if it wasn't set before running the test.
        if self.saved_filepath is None:
            if THINGSDB in os.environ:
                del os.environ[THINGSDB]
        else:
            os.environ[THINGSDB] = self.saved_filepath

    def test_get_tag_by_database_filepath(self):
        del os.environ[THINGSDB]
        tag_uuid = "Qt2AY87x2QDdowSn9HKTt1"
        tag = things.get(tag_uuid, filepath=TEST_DATABASE_FILEPATH)
        self.assertEqual(tag["uuid"], tag_uuid)  # type: ignore

    def test_get_url_scheme_auth_token(self):
        expected = "vKkylosuSuGwxrz7qcklOw"
        token = things.token()
        self.assertEqual(token, expected)

    def test_search(self):
        tasks = things.search("invalid_query")
        self.assertEqual(0, len(tasks))

        # test some special characters
        tasks = things.search("'")
        self.assertEqual(0, len(tasks))

        tasks = things.search('"')
        self.assertEqual(0, len(tasks))

        with self.assertRaises(ValueError):
            things.search("To-Do\0Heading")

        todos = things.search("To-Do % Heading", status=None)
        # Assert finds
        #   "To-Do in Heading",
        #   "Completed To-Do in Heading",
        #   "Canceled To-Do in Heading"
        self.assertEqual(3, len(todos))

    def test_inbox(self):
        tasks = things.inbox()
        self.assertEqual(2, len(tasks))

    def test_trashed(self):
        tasks = things.trash()
        self.assertEqual(5, len(tasks))
        todos = things.todos(trashed=True)
        self.assertEqual(2, len(todos))
        projects = things.projects(trashed=True)
        self.assertEqual(1, len(projects))
        projects = things.projects(trashed=None)
        self.assertEqual(4, len(projects))
        projects = things.trash(type="project")
        self.assertEqual(1, len(projects))

        projects = things.trash(type="project", include_items=True)
        project_items = projects[0]["items"]
        self.assertEqual(1, len(project_items))
        filtered_project_items = [
            item for item in project_items if "in Deleted Project" in item["title"]
        ]
        self.assertEqual(1, len(filtered_project_items))

        # TK: Add this test case to the database:
        # to-do with trashed = 1 and whose project also has trashed = 1.
        tasks = things.tasks(type="to-do", trashed=True, context_trashed=True)
        self.assertEqual(0, len(tasks))

    def test_upcoming(self):
        tasks = things.upcoming()
        self.assertEqual(1, len(tasks))

    def test_deadlines(self):
        tasks = things.deadlines()
        self.assertEqual(1, len(tasks))

    def test_today(self):
        tasks = things.today()
        self.assertEqual(3, len(tasks))

    def test_checklist(self):
        checklist_items = things.checklist_items("3Eva4XFof6zWb9iSfYy4ej")
        self.assertEqual(3, len(checklist_items))
        checklist_items = things.checklist_items("K9bx7h1xCJdevvyWardZDq")
        self.assertEqual(0, len(checklist_items))

    def test_anytime(self):
        tasks = things.anytime()
        self.assertEqual(12, len(tasks))
        self.assertTrue(any(task.get("area_title") == "Area 1" for task in tasks))

    def test_logbook(self):
        tasks = things.logbook()
        self.assertEqual(21, len(tasks))

    def test_canceled(self):
        tasks = things.canceled()
        self.assertEqual(11, len(tasks))

    def test_completed(self):
        tasks = things.completed()
        self.assertEqual(10, len(tasks))

    def test_someday(self):
        tasks = things.someday()
        self.assertEqual(1, len(tasks))

    def test_get_by_uuid(self):
        task = things.get("invalid_uuid")
        self.assertEqual(None, task)
        task = things.get("invalid_uuid", "NOT FOUND")
        self.assertEqual("NOT FOUND", task)
        task = things.get("Qt2AY87x2QDdowSn9HKTt1")
        self.assertEqual(4, len(task.keys()))  # type: ignore

    def test_todos(self):
        todos = things.todos(start="Anytime")
        self.assertEqual(8, len(todos))
        todos = things.todos(start="Anytime", status="completed")
        self.assertEqual(6, len(todos))
        todos = things.todos(status="completed")
        self.assertEqual(10, len(todos))
        todos = things.todos(include_items=True)
        self.assertEqual(12, len(todos))
        tasks = things.tasks(include_items=True)
        self.assertEqual(16, len(tasks))
        with self.assertRaises(ValueError):
            things.todos(status="invalid_value")
        todo = things.todos("A2oPvtt4dXoypeoLc8uYzY")
        self.assertEqual(16, len(todo.keys()))  # type: ignore

    def test_tags(self):
        tags = things.tags()
        self.assertEqual(5, len(tags))
        tags = things.tags(include_items=True)
        self.assertEqual(5, len(tags))
        tags = things.tasks(tag="Errand")
        self.assertEqual(1, len(tags))
        tag = things.tags(title="Errand")
        self.assertEqual("Errand", tag["title"])  # type: ignore

    def test_get_link(self):
        link = things.link("uuid")
        self.assertEqual("things:///show?id=uuid", link)

    def test_projects(self):
        projects = things.projects()
        self.assertEqual(3, len(projects))
        projects = things.projects(include_items=True)
        self.assertEqual(2, len(projects[0]["items"]))

    def test_areas(self):
        areas = things.areas()
        self.assertEqual(3, len(areas))
        areas = things.areas(include_items=True)
        self.assertEqual(3, len(areas))
        count = things.areas(count_only=True)
        self.assertEqual(3, count)
        with self.assertRaises(ValueError):
            things.areas("invalid_uuid")
        area = things.areas("Y3JC4XeyGWxzDocQL4aobo")
        self.assertEqual("Area 3", area["title"])  # type: ignore

    def test_database_version(self):
        version = things.Database().get_version()
        self.assertEqual(18, version)

    def test_last(self):
        last_tasks = things.last("0d")
        self.assertEqual(len(last_tasks), 0)

        last_tasks = things.last("10000w")
        self.assertEqual(len(last_tasks), 16)

        last_tasks = things.last("100y", status="completed")
        self.assertEqual(len(last_tasks), 10)

        with self.assertRaises(ValueError):
            things.last(None)

        with self.assertRaises(ValueError):
            things.last([])

        with self.assertRaises(ValueError):
            things.last("XYZ")

        with self.assertRaises(ValueError):
            things.last("")

        with self.assertRaises(ValueError):
            things.last("3X")

    def test_tasks(self):
        count = things.tasks(status="completed", last="100y", count_only=True)
        self.assertEqual(count, 10)

        # get task by uuid
        count = things.tasks(uuid="5pUx6PESj3ctFYbgth1PXY", count_only=True)
        self.assertEqual(count, 1)

        count = things.tasks(uuid="invalid_uuid", count_only=True)
        self.assertEqual(count, 0)

        with self.assertRaises(ValueError):
            things.tasks(uuid="invalid_uuid")

        # special characters
        tasks = things.tasks(area='"')
        self.assertEqual(len(tasks), 0)

        tasks = things.tasks(area="'")
        self.assertEqual(len(tasks), 0)

        with self.assertRaises(ValueError):
            things.tasks(area="\0")

    def test_database_details(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            things.areas(print_sql=True)
        self.assertTrue("ORDER BY" in output.getvalue())

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            database = things.database.Database()  # type: ignore
            database.debug = True
            database.get_tags()
        self.assertTrue("/* Filepath" in output.getvalue())


if __name__ == "__main__":
    unittest.main()
    ThingsCase()  # For Vulture
