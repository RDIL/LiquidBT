build: clean
	python3 setup.py sdist bdist_wheel 
.PHONY: build

install-dev: build
	python3 -m pip install --upgrade dist/*.tar.gz
.PHONY: install-dev

test: install-dev
	python3 -m pip install --upgrade dist/*.tar.gz
	cd testpackage && python3 liquidbt_config.py
.PHONY: test

static-analysis: clean
	mypy -p liquidbt -m liquidbt_i18n -p liquidbt_plugin_command_clean -p liquidbt_plugin_remove_prints
	black --check *.py --line-length 78
	black --check **/*.py --line-length 78
	flake8 **/*.py
.PHONY: static-analysis

clean:
	rm -rf *.egg-info build dist .mypy_cache
	cd testpackage && rm -rf testpackagerdil
.PHONY: clean
