MAIN=things
SRC_CORE=./things
SRC_TEST=tests
DST_DOCS=docs
PYTHON=python3
PYDOC=pydoc3
PIP=pip3
PIPENV=pipenv
PDOC=pdoc

DATE:=$(shell date +"%Y-%m-%d")
VERSION=$(shell $(PYTHON) -c 'import things; print(things.__version__)')

help: ## Print help for each target
	$(info Things low-level Python API.)
	$(info ============================)
	$(info )
	$(info Available commands:)
	$(info )
	@grep '^[[:alnum:]_-]*:.* ##' $(MAKEFILE_LIST) \
		| sort | awk 'BEGIN {FS=":.* ## "}; {printf "%-25s %s\n", $$1, $$2};'

run: ## Run the code
	@$(PYTHON) -m $(SRC_CORE).$(MAIN)

install: ## Install the code
	@$(PYTHON) setup.py install

uninstall: ## Uninstall the code
	@$(PIP) uninstall -y things

test: ## Test the code
	@type coverage >/dev/null 2>&1 || (echo "Run '$(PIP) install coverage' first." >&2 ; exit 1)
	@coverage erase
	@coverage run -a -m $(SRC_TEST).test_things
	@coverage report
	@coverage html

testdoc: ## Test the code within the documentation
	@type pytest >/dev/null 2>&1 || (echo "Run '$(PIP) install pytest' first." >&2 ; exit 1)
	THINGSDB=tests/main.sqlite pytest --doctest-modules

.PHONY: doc
doc: install ## Document the code
	@type pytest >/dev/null 2>&1 || (echo "Run '$(PIP) install pytest' first." >&2 ; exit 1)
	@#$(PYDOC) $(SRC_CORE).api
	@$(PDOC) -o $(DST_DOCS) -d numpy -n $(SRC_CORE)
	@echo "Now open $(DST_DOCS)"

.PHONY: clean
clean: ## Cleanup
	@rm -f $(DEST)
	@find . -name \*.pyc -delete
	@find . -name __pycache__ -delete
	@rm -rf htmlcov
	@rm -rf build dist *.egg-info .eggs
	@rm -rf .mypy_cache/ */.mypy_cache/
	@rm -f .coverage
	@rm -rf .tox

auto-style: ## Style the code
	@if type isort >/dev/null 2>&1 ; then isort . ; \
	 else echo "SKIPPED. Run '$(PIP) install isort' first." >&2 ; fi
	@if type autoflake >/dev/null 2>&1 ; then autoflake -r --in-place --remove-unused-variables . ; \
	 else echo "SKIPPED. Run '$(PIP) install isort' first." >&2 ; fi
	@if type black >/dev/null 2>&1 ; then black . ; \
	 else echo "SKIPPED. Run '$(PIP) install black' first." >&2 ; fi

code-style: ## Test the code style
	@echo Pycodestyle...
	@if type pycodestyle >/dev/null 2>&1 ; then pycodestyle *.py $(SRC_CORE)/*.py $(SRC_TEST)/*.py ; \
	 else echo "SKIPPED. Run '$(PIP) install pycodestyle' first." >&2 ; fi
	@echo Pydocstyle...
	@if type pydocstyle >/dev/null 2>&1 ; then pydocstyle $(SRC_CORE)/*.py $(SRC_TEST)/*.py ; \
	 else echo "SKIPPED. Run '$(PIP) install pydocstyle' first." >&2 ; fi

code-count: ## Count the code
	@if type cloc >/dev/null 2>&1 ; then cloc $(SRC_CORE) ; \
	 else echo "SKIPPED. Run 'brew install cloc' first." >&2 ; fi

code-lint: code-style ## Lint the code
	@echo Pylama...
	@if type pylama >/dev/null 2>&1 ; then pylama *.py $(SRC_CORE)/*.py $(SRC_TEST)/*.py ; \
	 else echo "SKIPPED. Run '$(PIP) install pylama' first." >&2 ; fi
	@echo Pylint...
	@if type pylint >/dev/null 2>&1 ; then pylint -sn *.py $(SRC_CORE) $(SRC_TEST) ; \
	 else echo "SKIPPED. Run '$(PIP) install pylint' first." >&2 ; fi
	@echo Flake...
	@if type flake8 >/dev/null 2>&1 ; then flake8 . ; \
	 else echo "SKIPPED. Run '$(PIP) install flake8' first." >&2 ; fi
	@echo Pyright...
	@if type pyright >/dev/null 2>&1 ; then PYRIGHT_PYTHON_FORCE_VERSION=latest pyright  *.py $(SRC_CORE) $(SRC_TEST) ; \
	 else echo "SKIPPED. Run 'npm install -f pyright' first." >&2 ; fi
	@echo MyPy...
	@if type mypy >/dev/null 2>&1 ; then mypy --no-error-summary --ignore-missing-imports *.py $(SRC_CORE) $(SRC_TEST) ; \
	 else echo "SKIPPED. Run '$(PIP) install mypy' first." >&2 ; fi
	@echo Vulture...
	@if type vulture >/dev/null 2>&1 ; then vulture *.py $(SRC_CORE)/*.py $(SRC_TEST)/*.py --exclude conftest.py; \
	 else echo "SKIPPED. Run '$(PIP) install vulture' first." >&2 ; fi

lint: code-style code-lint  ## Lint everything

deps-install: ## Install the dependencies
	@type $(PIPENV) >/dev/null 2>&1 || (echo "Run e.g. 'brew install pipenv' first." >&2 ; exit 1)
	@$(PIPENV) install --dev
	npm install pyright

feedback: ## Give feedback
	@open https://github.com/thingsapi/things.py/issues

release: build ## Create a new release
	@type gh >/dev/null 2>&1 || (echo "Run e.g. 'brew install gh' first." >&2 ; exit 1)
	@echo "Checking for not committed changes..."
	@git diff --exit-code && git diff --cached --exit-code
	@echo "########################"
	@echo Making release for version "$(VERSION)". Press ENTER to continue...
	@echo "########################"
	@read
	@gh release create "v$(VERSION)" -t "Release $(VERSION) ($(DATE))" 'dist/$(MAIN).py-$(VERSION).tar.gz'

build: clean ## Build the code
	@$(PYTHON) setup.py sdist bdist_wheel

upload: build ## Upload the code
	@type twine >/dev/null 2>&1 || (echo "Run e.g. 'pip install twine' first." >&2 ; exit 1)
	@echo "########################"
	@echo "Using ~/.pypirc or environment variables TWINE_USERNAME and TWINE_PASSWORD"
	@echo "See: https://packaging.python.org/specifications/pypirc/#using-a-pypi-token"
	@echo "########################"
	@twine upload dist/things.py*

db-to-things:
	@cp tests/main.sqlite* ~/Library/Group\ Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-*/Things\ Database.thingsdatabase/

db-from-things:
	@cp ~/Library/Group\ Containers/JLMPQHK86H.com.culturedcode.ThingsMac/ThingsData-*/Things\ Database.thingsdatabase/main.sqlite* tests

info:
	pipenv --venv
