dev: clean
	cd .. && python3 setup.py sdist bdist_wheel && python3 -m pip install --upgrade dist/*.tar.gz && cd testpackage && python3 liquidbt_config.py
.PHONY: dev

clean:
	cd .. && rm -rf *.egg-info build dist && cd testpackage && rm -rf slots testpackagerdil slots.*
.PHONY: clean
