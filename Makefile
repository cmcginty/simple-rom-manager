.PHONY: all clean dist help init install lint pylintrc requirements test \
	upgrade-requiements

SOURCES := setup.py
PYLINT_ARGS :=
PEP8_ARGS := --max-line-length=100

help:
	@echo 'Help Instructions:'
	@echo
	@echo '  CI/CD Workflow'
	@echo '  --------------'
	@echo '  all                   Run all test/lint cycle'
	@echo '  test                  Run unit/integration tests'
	@echo '  lint                  Run linters'
	@echo '  dist                  Build PyPi distribution'
	@echo '  clean                 Remove temp files'
	@echo
	@echo '  Dev Workspace'
	@echo '  -------------'
	@echo '  init                  Reset dependencies to specified versions'
	@echo '  requirements          Freeze all dependencies to requirements.txt'
	@echo '  upgrade-requirements  Upgrade all depdendencies versions; run "make init" to install'
	@echo '  pylintrc              Upgrade auto-generated pylintrc'

init:
	pip install --upgrade pip setuptools
	pip install --upgrade pip-tools
	pip-sync dev-requirements.txt requirements.txt

requirements:
	pip-compile setup.py --output-file requirements.txt
	pip-compile dev-requirements.in

upgrade-requirements:
	pip-compile -U setup.py --output-file requirements.txt
	pip-compile -U dev-requirements.in

.DEFAULT_GOAL := all
all: test lint

test:

lint:
	pep8 ${PEP8_ARGS} ${SOURCES}
	pylint ${PYLINT_ARGS} ${SOURCES}

clean:
	- rm -r dist/ *.egg-info/

dist:
	python3 setup.py sdist

install:
	python3 setup.py install
	if ! [ -z $${VIRTUAL_ENV+x} ]; then pyenv rehash; fi

# NOTE: sponge can be installed from "moreutils" package
pylintrc:
	pylint --generate-rcfile | sponge pylintrc
