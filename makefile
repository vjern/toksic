.ONESHELL:

test:
	python -m pytest --cov=toksic --cov-report term-missing  tests -vvv

lint:
	# git ls-files for local files
	git ls-tree --full-tree -r --name-only HEAD \
	| grep ".py$$" \
	| xargs flake8 --max-line-length=100
