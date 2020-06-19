.PHONY: dist
dist:
	@python setup.py sdist

.PHONY: build
build:
	@python setup.py build

.PHONY: install
install:
	@python setup.py install

.PHONY: push
push:
	@python setup.py sdist upload -r pypi
