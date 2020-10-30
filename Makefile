test:
	pytest -vv --show-capture=all

ci:
	pytest --show-capture=all --cov=starlette_dataframe_response --no-cov-on-fail --cov-report term-missing
	$(MAKE) lint typing

format:
#	pip install -e .[dev]
	black starlette_dataframe_response setup.py

# https://www.flake8rules.com/rules/W503.html
# https://www.flake8rules.com/rules/E203.html
# https://www.flake8rules.com/rules/E501.html
lint:
#	pip install -e .[dev]
	flake8 starlette_dataframe_response --ignore W503,E203,E501

typing:
#	pip install -e .[dev]
	mypy --strict --strict-equality --ignore-missing-imports starlette_dataframe_response
mypy: typing

build:
#	pip install wheel
	python setup.py sdist bdist_wheel

upload:
#	pip install twine
	twine check dist/starlette-dataframe-response-$(shell cat VERSION)*
	twine upload dist/starlette-dataframe-response-$(shell cat VERSION)*

.PHONY: test ci format lint typing mypy build upload
