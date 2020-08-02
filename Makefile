.DEFAULT_GOAL := install
init:
	virtualenv --no-site-packages venv
	source venv/bin/activate
	pip install -r requirements.txt
	python -m ipykernel install --user --name venv --display-name  venv_a1chemy

test:
	py.test tests

clean:
	rm -rf build dist a1chemy.egg-info

install:
	python setup.py install
	rm -rf build dist a1chemy.egg-info