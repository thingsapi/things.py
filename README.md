# Things Python API

A simple Python 3 library to read your [Things app](https://culturedcode.com/things) data.

[![Build Status](https://github.com/thingsapi/things.py/workflows/Build-Test/badge.svg)](https://github.com/thingsapi/things.py/actions)
[![Coverage Status](https://coveralls.io/repos/github/thingsapi/things.py/badge.svg?branch=master)](https://coveralls.io/github/thingsapi/things.py?branch=master)
[![GitHub Release](https://img.shields.io/github/v/release/thingsapi/things.py?sort=semver)](https://github.com/thingsapi/things.py/releases)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/things?label=pypi%20downloads)](https://pypi.org/project/things/)
[![GitHub Download Count](https://img.shields.io/github/downloads/thingsapi/things.py/total.svg)](https://github.com/thingsapi/things.py/releases)
[![GitHub Issues](https://img.shields.io/github/issues/thingsapi/things.py)](https://github.com/thingsapi/things.py/issues)
[![Scrutinizer Code Quality](https://img.shields.io/scrutinizer/quality/g/thingsapi/things.py)](https://scrutinizer-ci.com/g/thingsapi/things.py/?branch=master)

## Table of Contents

- [Install](#install)
- [Examples](#examples)
- [Background](#background)
- [Things URLs](#things-urls)

## Install

```sh
$ pip3 install things.py
# or
$ git clone https://github.com/thingsapi/things.py && cd things.py && make install
```

## Examples

```python
>>> import things
>>> things.tasks()
[{'uuid': '2Ukg8I2nLukhyEM7wYiBeb',
  'title': 'Make reservation for dinner',
  'type': 'task',
  'project': 'bNj6TPdKYhY6fScvXWVRDX',
  ...},
 {'uuid': 'RLZroza3jz0XPs3uAlynS7',
  'title': 'Buy a whiteboard and accessories',
  'type': 'task',
  'project': 'w8oSP1HjWstPin8RMaJOtB',
  'notes': "Something around 4' x 3' that's free-standing, two-sided, and magnetic.",
  'checklist': True,
  ...
>>> things.tasks('RLZroza3jz0XPs3uAlynS7')
{'uuid': 'RLZroza3jz0XPs3uAlynS7',
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
  'title': 'Throw Birthday Party',
  'type': 'project',
  'area': 'bNj6TPdKYhY6fScvXWVRDX',
  ...},
 {'uuid': 'w8oSP1HjWstPin8RMaJOtB',
  'title': 'Set Up Home Office',
  'type': 'project',
  'area': 'Gw9QefIdgR6nPEoY5hBNSh',
  ...

>>> things.areas()
[{'uuid': 'ToLxnnBrWkfHC3tkx4vxdV',
  'title': 'Family',
  'type': 'area',
  ...},
 {'uuid': 'Gw9QefIdgR6nPEoY5hBNSh',
  'title': 'Apartment',
  'type': 'area',
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

The task management app Things stores all your to-dos in a SQLite database file (details [here](https://culturedcode.com/things/support/articles/2982272/#get-the-things-3-database-file)). This format is machine-readable, not human-readable. The aim of this project is let you access all your data in a human-readable way. We thereby stay as true to the database as possible while doing SQL Joins and transformations to aid understanding of the data.

Here's the terminology used involving the database:

- area
- tag
- Task (capitalized)
  - type
    - `"task"`: Task in a project or a non-project Task; can have a checklist; can link to an area and tags.
    - `"project"`: a large Task; can have (sub)"tasks" and headings; can link to an area and tags.
    - `"heading"`: contained within a project in order to group "tasks"
  - status:  `"incomplete"`,  `"canceled"`, or `"completed"`
  - trashed: `True` or `False`
- checklist item (contained within a "task")


## Things URLs

You can make good use of the `uuid` to link to tasks, areas, tags, and more from other apps. Read more [here](https://culturedcode.com/things/blog/2018/02/hey-things/).
