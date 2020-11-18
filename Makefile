.DEFAULT_GOAL := install

test:
	py.test tests

clean:
	rm -rf build dist a1chemy.egg-info

update_requirements:
	pip freeze | grep -v 'a1chemy' > requirements.txt

install:
	python setup.py install
	rm -rf build dist a1chemy.egg-info