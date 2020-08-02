init:
	virtualenv --no-site-packages venv
	source venv/bin/activate
	python -m ipykernel install --user --name venv --display-name  venv_a1chemy
    pip install -r requirements.txt
install:
    python setup.py install
test:
    py.test tests
clean:
    

.PHONY: init test