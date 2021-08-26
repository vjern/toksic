.ONESHELL:

test:
	python -m pytest --cov=toksic --cov-report term-missing  tests -vvv

%:
	python -m neni examples/$*.nn