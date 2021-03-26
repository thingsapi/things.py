# -*- coding: utf-8 -*-

"""
Module implementing Things API
"""


from .database import Database


def tasks(
    type="task",
    status="incomplete",
    start=None,
    area=None,
    project=None,
    heading=None,
    start_date=None,
    index="index",
    include_items=False,
    **kwargs
):
    """
    Read tasks into a list of dicts.

    Parameters
    ----------
    type : {'task', 'project', 'heading', None}, optional, default 'task'
        Only return a specific type of Task:

        'task':     Default. Task within a project or a standalone task;
                    can link to an area, tags, and a checklist.
        'project':  a supertask; can link to an area, tags, (sub)tasks,
                    and headings.
        'heading':  a group of tasks; links to a project.
        None:       Return any type of task.

    status : {'incomplete', 'completed', 'canceled', None}, optional, \
        default 'incomplete'

        Only include tasks matching that status. If the argument is `None`,
        then include tasks with any status value.

    start : {'Inbox', 'Anytime', 'Someday', None}, optional
        Only include tasks matching that start value. If the argument is
        `None` (default), then include tasks with any start value.

    area : str, bool, or None, optional
        Any valid uuid of an area. Only include tasks matching that area.
        If the argument is `False`, only include tasks _without_ an area.
        If the argument is `True`, only include tasks _with_ an area.
        If the argument is `None`, then ignore the area value, that is,
        include tasks both with and without a containing area.

    project : str or None, optional
        Any valid uuid of a project. Only include tasks matching that project.
        If the argument is `False`, only include tasks _without_ a project.
        If the argument is `True`, only include tasks _with_ a project.
        If the argument is `None`, then ignore the project value, that is,
        include tasks both with and without a containing project.

    heading : str or None, optional
        Any valid uuid of a heading. Only include tasks matching that heading.
        If the argument is `False`, only include tasks _without_ a heading.
        If the argument is `True`, only include tasks _with_ a heading.
        If the argument is `None`, then ignore the heading value, that is,
        include tasks both with and without a containing heading.

    start_date : bool or None, optional
        If the argument is `False`, only include tasks _without_ a start date.
        If the argument is `True`, only include tasks _with_ a start date.
        If the argument is `None`, then ignore the start date value, that is,
        include tasks both with and without a start date.

    include_items : boolean, default False
        Include tasks in projects and headings.

    index : {'index', 'todayIndex'}, default 'index'
        Database index to order result by.

    **kwargs : optional
        Optional keyword arguments passed to ``Database``.

    Returns
    -------
    list
        A list of dicts representing Things tasks.

    Examples
    --------
    >>> things.tasks()
    >>> things.tasks(area='hIo1FJlAYGKt1Yj38vzKc3', include_items=True)
    """
    database = Database(**kwargs)
    result = database.get_tasks(
        type=type,
        status=status,
        start=start,
        area=area,
        project=project,
        heading=heading,
        start_date=start_date,
        index=index,
    )

    if include_items:
        for item in result:
            if item["type"] == "project":
                project = item
                # add items of project
                project["items"] = items = tasks(
                    type=None, project=project["uuid"], include_items=True, **kwargs
                )
                # tasks without headings appear before headings
                items.sort(key=lambda item: item["type"], reverse=True)
            elif item["type"] == "heading":
                heading = item
                heading["items"] = tasks(heading=heading["uuid"], **kwargs)

    return result


def areas(include_items=False, **kwargs):
    """
    Read areas into a list of dicts.

    Parameters
    ----------
    include_items : boolean, default False
        Include tasks and projects in each area.

    **kwargs : optional
        Optional keyword arguments passed to ``Database`` and `things.tasks`.

    Returns
    -------
    list
        A list of dicts representing Things areas.

    Examples
    --------
    >>> things.areas()
    >>> things.areas(include_items=True, status='completed')
    """
    database = Database(filepath=kwargs.get("filepath"))
    result = database.get_areas()
    if include_items:
        for area in result:
            area["items"] = tasks(
                type=None, area=area["uuid"], include_items=True, **kwargs
            )
    return result


def tags(**kwargs):
    database = Database(**kwargs)
    return database.get_tags()


# Utility functions derived from above


def canceled(**kwargs):
    return tasks(type=None, status="canceled", **kwargs)


def completed(**kwargs):
    return tasks(type=None, status="completed", **kwargs)


def inbox(**kwargs):
    return tasks(start="Inbox", **kwargs)


def projects(**kwargs):
    return tasks(type="project", **kwargs)


def today(**kwargs):
    return tasks(type=None, start_date=True, index="todayIndex", **kwargs)
