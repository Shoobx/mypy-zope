VE=ve
VEBIN=$(VE)/bin

all: $(VE)

$(VE): setup.py
	python3 -m venv $(VE)
	$(VEBIN)/pip install -e .[test]

.PHONY: test
test:
	$(VEBIN)/pytest -v --cov src/mypy_zope --cov-report=html --cov-report=term


# Mypy self-test
.PHONY: mypy
mypy:
	$(VEBIN)/mypy src/mypy_zope --strict

.PHONY: mypy-report
mypy-report:
	$(VEBIN)/mypy src/mypy_zope --strict --html-report reports/html --txt-report reports/txt
	cat reports/txt/index.txt
