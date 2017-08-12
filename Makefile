SOURCES := $(wildcard *.py) srm/
$(info $(SOURCES))
PYLINT_ARGS :=
PEP8_ARGS := --max-line-length=100

.PHONY: help
help:
	@echo 'Help Instructions:'
	@echo
	@echo '  CI/CD Workflow'
	@echo '  --------------'
	@echo '  all            Run all test/lint cycle'
	@echo '  test           Run unit/integration tests'
	@echo '  lint           Run linters'
	@echo '  dist           Build PyPi distribution'
	@echo '  clean          Remove temp files'
	@echo
	@echo '  Dev Workspace'
	@echo '  -------------'
	@echo '  init           Reset dependencies to specified versions'
	@echo '  deps           Freeze all dependencies to requirements.txt'
	@echo '  deps-upgrade   Upgrade all depdendencies versions; run "make init" to install them'
	@echo '  pylintrc       Upgrade auto-generated pylintrc'

.PHONY: init
init:
	pip install --upgrade pip setuptools
	pip install --upgrade pip-tools
	pip-sync dev-requirements.txt requirements.txt

.PHONY: deps
deps:
	PYTHONPATH=. pip-compile setup.py --output-file requirements.txt
	pip-compile dev-requirements.in

.PHONY: deps-upgrade
deps-upgrade:
	PYTHONPATH=. pip-compile -U setup.py --output-file requirements.txt
	pip-compile -U dev-requirements.in

.PHONY: all
.DEFAULT_GOAL := all
all: test lint mypy

.PHONY: test
test:
	python -m unittest discover -f

.PHONY: lint
lint:
	pep8 ${PEP8_ARGS} ${SOURCES}
	pylint ${PYLINT_ARGS} ${SOURCES}

.PHONY: mypy
mypy:
	mypy --strict ${SOURCES}

.PHONY: clean
clean:
	- rm -r dist/ *.egg-info/ .mypy_cache

.PHONY: dist
dist:
	python3 setup.py check sdist

# NOTE: sponge can be installed from "moreutils" package
.PHONY: pylintrc
pylintrc:
	pylint --generate-rcfile | sponge pylintrc

git_version    = $(shell git describe --abbrev=0)
next_patch_ver = $(shell python versionbump.py --patch $(call git_version))
next_minor_ver = $(shell python versionbump.py --minor $(call git_version))
next_major_ver = $(shell python versionbump.py --major $(call git_version))

.PHONY: release
release: test lint mypy dist
	git tag -a $(call next_patch_ver)
	git push origin master --tags
	python3 setup.py upload
