# Contributing to things.py

Thank you for considering contributing to things.py! Here are some pointers to help you get started.

## Have you found an issue?

Check out the [list of open issues](https://github.com/thingsapi/things.py/issues) first, to make sure it hasn't already been reported.

If it has not, [submit a bug report](https://github.com/thingsapi/things.py/issues/new/choose). Provide a list of steps to reproduce the issue and the expected outcome.

## Have an idea for a feature?

[Submit a feature request](https://github.com/thingsapi/things.py/issues/new/choose). Include the goal of the new feature, (ideally) a suggested approach, and any additional context.

## Want to fix an issue?

Read below for guidance on setting up a local environment and testing.

### Setting up your environment

#### 1. Clone the repo

Run:
```sh
git clone git@github.com:thingsapi/things.py.git
```

#### 2. Create a virtual environment

A virtual environment allows you to install and upgrade Python distribution packages without interfering with the behaviour of other Python applications running on your system. You will probably want to do this before you run all the test targets, which require additional Python packages to be installed.

Follow the [official Python documentation](https://docs.python.org/3/tutorial/venv.html) to create a virtual environment:
```sh
python3 -m venv venv
source venv/bin/activate
```

#### 3. Start development

Start work on your pull request (PR).

## Pull request process

- Open a GitHub pull request with the patch.
- Ensure the PR description clearly describes the problem and solution. Link to the relevant issue, if applicable.
- Generally speaking, pull requests require `test_script.py` to be updated to ensure changes to the code and new features have test coverage. Sometimes, the test database itself needs to be updated; see [here](#working-with-the-test-things-database) for guidance.

### Run tests

Run:
```sh
make test
```

Add any additional tests required, [updating the Test Things database](#working-with-the-test-things-database) if neccessary.

### Validate documentation examples

Examples in the documentation should produce the expected results with your changes. Any documentation examples you've added should pass these tests as well.
```sh
make testdoc
```

### Check linting compliance

Ensure code changes comply with linting rules. Make any necessary changes based on the linting report run when executing:
```sh
make lint
```

### Other Make targets

Run `make help` to see the full list of targets available in the [Makefile](https://github.com/thingsapi/things.py/blob/master/Makefile) that may be helpful.

## Working with the Test Things Database

For tests, sometimes the test database needs to be updated. Confirming your changes work against your own Things database is one thing, but for everybody else to see the effects of your change, they need to be tested with the Things test database included with things.py. Here's how you update said database if needed.

### 1. Back up your own Things database

Your local (personal) Things app's database will be replaced with the Test database, so you will want to make a backup.

Following [these instructions](https://culturedcode.com/things/support/articles/2803570/), effectively all you need to do is close the Things app, and make a copy of this folder:

```
~/Library/Group Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-xxxxx/Things Database.thingsdatabase
```

...where the `xxxxx` portion is a unique combination of letters and numbers.

### 2. Copy the test database to your Things app folder

⚠️ _Before you proceed, make sure you've actually backed up your own personal database per step 1._

In the things.py repo folder, run this command to copy the test database over top of your local Things database:

```sh
make db-to-things
```

### 3. Make changes if necessary

Launch the Things app, and you should see the test tasks and projects, instead of your own tasks.

Confirm there isn't already a task, project, or other Things object that you can test your change(s) against.

If you need to make changes to say the `createdDate`, you'll need to open the database with `sqlite3` or another tool that can update SQLite databases. Changes to the test database may require schema knowledge. Reading the `things.py` documentation and code can help with that.

### 4. Copy the test database back from your Things app folder

If you had to make changes to the test database, update the test database in the project by running this command to copy the local Things database to the `tests` folder:

```sh
make db-from-things
```

Make sure to include the updated `.thingsdatabase` file in your PR.

### 5. Restore your personal Things database

Once your PR has been submitted, you should be able to restore your personal Things database simply by:

1. Closing the Things app.
2. Copy the `Things Database.thingsdatabase` folder you backed up into your local Library folder. 
3. If required, you may have to log back into Things Cloud, as todos may have changed on other devices during development, and to make sure you're back in sync.
