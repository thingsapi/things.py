# Things Python API

_things.py_ is a simple Python 3 library to read data from your [Things app](https://culturedcode.com/things).

[![GitHub Release](https://img.shields.io/github/v/release/thingsapi/things.py?sort=semver)](https://github.com/thingsapi/things.py/releases)
[![Build Status](https://github.com/thingsapi/things.py/workflows/Build-Test/badge.svg)](https://github.com/thingsapi/things.py/actions)
[![Coverage Status](https://codecov.io/gh/thingsapi/things.py/branch/main/graph/badge.svg?token=DBWGKAEYAP)](https://codecov.io/gh/thingsapi/things.py)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=thingsapi_things.py&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=thingsapi_things.py)
[![GitHub Issues](https://img.shields.io/github/issues/thingsapi/things.py)](https://github.com/thingsapi/things.py/issues)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/things.py?label=pypi%20downloads)](https://pypi.org/project/things.py/)
[![GitHub Download Count](https://img.shields.io/github/downloads/thingsapi/things.py/total.svg)](https://github.com/thingsapi/things.py/releases)

## Table of Contents

- [Install](#install)
- [Examples](#examples)
- [Documentation](#documentation)
- [Background](#background)
- [Things URL Scheme](#things-url-scheme)
- [Used By](#used-by)

## Install

```sh
$ pip3 install things.py
# or
$ git clone https://github.com/thingsapi/things.py && cd things.py && make install
```

## Examples

```python
>>> import things
>>> things.todos()
[{'uuid': '2Ukg8I2nLukhyEM7wYiBeb',
  'type': 'to-do',
  'title': 'Make reservation for dinner',
  'project': 'bNj6TPdKYhY6fScvXWVRDX',
  ...},
 {'uuid': 'RLZroza3jz0XPs3uAlynS7',
  'type': 'to-do',
  'title': 'Buy a whiteboard and accessories',
  'project': 'w8oSP1HjWstPin8RMaJOtB',
  'notes': "Something around 4' x 3' that's free-standing, two-sided, and magnetic.",
  'checklist': True,
  ...
>>> things.todos('RLZroza3jz0XPs3uAlynS7')
{'uuid': 'RLZroza3jz0XPs3uAlynS7',
 'type': 'to-do',
 'title': 'Buy a whiteboard and accessories',
 ...
 'checklist': [
     {'title': 'Cleaning Spray', 'status': 'completed', ...},
     {'title': 'Magnetic Eraser', 'status': 'incomplete', ...},
     {'title': 'Round magnets', 'status': 'incomplete', ...}
 ]
 ...
}

>>> things.projects()
[{'uuid': 'bNj6TPdKYhY6fScvXWVRDX',
  'type': 'project',
  'title': 'Throw Birthday Party',
  'area': 'bNj6TPdKYhY6fScvXWVRDX',
  ...},
 {'uuid': 'w8oSP1HjWstPin8RMaJOtB',
  'type': 'project',
  'title': 'Set Up Home Office',
  'area': 'Gw9QefIdgR6nPEoY5hBNSh',
  ...

>>> things.areas()
[{'uuid': 'ToLxnnBrWkfHC3tkx4vxdV',
  'type': 'area',
  'title': 'Family',
  ...},
 {'uuid': 'Gw9QefIdgR6nPEoY5hBNSh',
  'type': 'area',
  'title': 'Apartment',
  ...

>>> things.tags()
[{'uuid': 'CKILg3kKF2jlCRisNFcqOj',
  'type': 'tag',
  'title': 'Home',
  'shortcut': None},
 {'uuid': 'gfmpz8zxnyfqMDvRi3E8vo',
  'type': 'tag',
  'title': 'Office',
  'shortcut': None},
 ...

>>> things.get('CKILg3kKF2jlCRisNFcqOj')
{'uuid': 'CKILg3kKF2jlCRisNFcqOj',
  'type': 'tag',
  'title': 'Home',
  'shortcut': None}

```

## Background

The task management app Things stores all your to-dos in a SQLite database file (details [here](https://culturedcode.com/things/support/articles/2982272/#get-the-things-3-database-file)). This format is intended to be machine-readable, not human-readable. The aim of this project is to let you access all your Things data in a human-readable way. We thereby stay as true to the database as possible while doing SQL joins and transformations to aid understanding of the data. Note that you can print the SQL used by adding the parameter `print_sql=True` to most API calls.

If any aspect of the API seems overly complex or doesn't meet your needs, please don't hesitate to add a new issue [here](https://github.com/thingsapi/things.py/issues).

### Terminology

Here are the core technical terms used involving the database:

- area
- tag
- task
  - type
    - `'to-do'`: can have checklists;
    - `'project'`: can have to-dos and headings;
    - `'heading'`:  part of a project; groups to-dos.
  - status:  `'incomplete'`,  `'canceled'`, or `'completed'`
  - trashed: `True` or `False`
  - start: `'Inbox'`, `'Anytime'`, or `'Someday'`
- checklist item (contained within a to-do)

## Documentation

The full documentation for this library can be found here: https://thingsapi.github.io/things.py/things/api.html

## Things URL Scheme

You can make good use of the `uuid` to link to to-dos, areas, tags, and more from other apps. Also updates are possible. Read an introduction [here](https://culturedcode.com/things/blog/2018/02/hey-things/) and see the documentation [here](https://culturedcode.com/things/help/url-scheme/).

## Contributing

We welcome contributions to things.py! Before submitting a pull request, please take a moment to look over the [contributing guidelines](https://github.com/thingsapi/things.py/blob/main/CONTRIBUTING.md) first.

## Used By

The following open-source projects make use of this library:

- [Asana to Things (ryansteed)](https://github.com/ryansteed/asana-to-things)
- [Things to CSV (nathankoerschner)](https://github.com/nathankoerschner/things_to_csv)
- [Things to Markdown (chrisgurney)](https://github.com/chrisgurney/things2md)
- [Things to Notion (Avery2)](https://github.com/Avery2/things3notionscript)
- [Things to Notion (MrAsynchronous)](https://github.com/MrAsynchronous/things3-to-notion-sync)
- [Things to Org file (chrizel)](https://github.com/chrizel/things-to-org)
- [KanbanView (AlexanderWillner)](https://github.com/AlexanderWillner/KanbanView)
- [Things CLI](https://github.com/thingsapi/things-cli)
- [things-3-report (CaAlden)](https://github.com/CaAlden/things-3-report)
- [ThingsReview (minthemiddle)](https://github.com/minthemiddle/things-review-py)
- [ThingsStats (lmgibson)](https://github.com/lmgibson/ThingsStats)
