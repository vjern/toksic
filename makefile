.ONESHELL:

test:
	python -m pytest tests -vvv

%:
	python -m neni examples/$*.nn