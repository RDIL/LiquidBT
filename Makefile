build: clean
	python3 setup.py sdist bdist_wheel 
	python3 -m pip install --upgrade dist/*.whl
.PHONY: build

test: build
	cd testpackage && python3 build.py
.PHONY: test

static-analysis: clean
	mypy -p liquidbt -m liquidbt_i18n -p liquidbt_plugin_command_clean -p liquidbt_plugin_remove_prints
	black --check *.py --line-length 78
	black --check **/*.py --line-length 78
	flake8 **/*.py
.PHONY: static-analysis

format:
	black *.py --line-length 78
	black **/*.py --line-length 78
.PHONY: format

clean:
	rm -rf *.egg-info build dist .mypy_cache *.egg-info
	cd testpackage && rm -rf testpackagerdil build dist
.PHONY: clean
