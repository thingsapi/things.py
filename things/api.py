# -*- coding: utf-8 -*-

"""
Module implementing Things API
"""


from .database import Database

# todo: type validation or similar (avoid invalid stroings)
def tasks(type="task", status="open", area=None,
          project=None, heading=None, **kwargs):
    """
    Read tasks into a list of dicts.

    Parameters
    ----------
    type : {'task', 'project', None}, optional, default 'task'
        Only return a specific type of Task:

        'task':     Default. Task within a project or a standalone task;
                    can link to an area, tags, and a checklist.
        'project':  a supertask; can link to an area, tags, (sub)tasks,
                    and headings.
        None:       Return both types 'task' and type 'project'.

        Note that the type 'heading' is implicitly included as part of
        the type 'project'.

    status : {'open', 'done', 'canceled', None}, optional, default 'open'
        Only include tasks matching that status. If the argument is `None`,
        then include tasks with any status value.

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

    **kwargs : optional
        Optional keyword arguments passed to ``Database``.

    Returns
    -------
    list
        A list of dicts representing Things tasks.

    Examples
    --------
    >>> things.tasks()
    """
    database = Database(**kwargs)
    if type == "task":
        return database.get_task(
            status=status, area=area, project=project, heading=heading
        )
    elif type == "project":
        result = []
        matched_projects = database.get_projects(status=status, area=area)
        for project in matched_projects:
            # group tasks by heading
            project["tasks"] = tasks(
                status=status, project=project["uuid"], heading=False
            )
            project["headings"] = {
                heading["title"]: tasks(status=status, heading=heading["uuid"])
                for heading in database.get_headings(
                    status=status, project=project["uuid"]
                )
            }
            result.append(project)
        return result


def areas(include_tasks=False, status="open", **kwargs):
    """
    Read areas into a list of dicts.

    Parameters
    ----------
    include_tasks : boolean, default False
        Include tasks and projects for each area.

    status : {'open', 'done', 'canceled', None}, default 'open'
        Include only tasks and projects with the specified status.
        The argument `None` includes all statuses.

    **kwargs : optional
        Optional keyword arguments passed to ``Database``.

    Returns
    -------
    list
        A list of dicts representing Things areas.

    Examples
    --------
    >>> things.areas()
    >>> things.areas(include_tasks=True, status='done')
    """
    database = Database(**kwargs)
    all_areas = database.get_areas()
    if include_tasks is False:
        return all_areas
    else:
        return [
            {
                **area,
                **dict(
                    projects=projects(area=area["uuid"]),
                    tasks=tasks(area=area["uuid"], project=False),
                ),
            }
            for area in all_areas
        ]


def tags(**kwargs):
    database = Database(**kwargs)
    return database.get_tags()


# Utility functions derived from above


def projects(**kwargs):
    return tasks(type="project", **kwargs)
