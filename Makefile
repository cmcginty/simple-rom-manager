MODULE := srm
SOURCES := $(wildcard *.py) ${MODULE}/
PYLINT_ARGS := --ignore=_version.py
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
	@echo '  release        Increase v0.0.X and deploy project to GitHub and PyPi'
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
	pip-compile setup.py --output-file requirements.txt
	pip-compile dev-requirements.in

.PHONY: deps-upgrade
deps-upgrade:
	pip-compile -U setup.py --output-file requirements.txt
	pip-compile -U dev-requirements.in

# NOTE: sponge can be installed from "moreutils" package
.PHONY: pylintrc
pylintrc:
	pylint --generate-rcfile | sponge pylintrc

.PHONY: all
.DEFAULT_GOAL := all
all: test lint mypy

.PHONY: test
test:
	python3 -m unittest discover -f

.PHONY: lint
lint:
	pep8 ${PEP8_ARGS} ${SOURCES}
	pylint ${PYLINT_ARGS} ${SOURCES}

.PHONY: mypy
mypy:
	mypy --strict ${SOURCES}

.PHONY: clean
clean:
	- rm -r dist/ build/ *.egg-info/ .mypy_cache

# remove optional trailing hash "v1.0-N-HASH" -> "v1.0-N"
git_describe_ver = $(shell git describe --tags | sed -E '/-/ s/(.*)-.*/\1/')
git_tag_ver      = $(shell git describe --abbrev=0)
next_patch_ver = $(shell python3 versionbump.py --patch $(call git_tag_ver))
next_minor_ver = $(shell python3 versionbump.py --minor $(call git_tag_ver))
next_major_ver = $(shell python3 versionbump.py --major $(call git_tag_ver))

.PHONY: ${MODULE}/_version.py
${MODULE}/_version.py:
	echo '__version__ = "$(call git_describe_ver)"' > $@

.PHONY: dist
dist: ${MODULE}/_version.py
	python3 setup.py check sdist

.PHONY: release
release: all
	git tag -a $(call next_patch_ver)
	git push origin master --tags
	$(MAKE) ${MODULE}/_version.py
	python3 setup.py check sdist upload
