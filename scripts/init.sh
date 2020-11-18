#!/bin/bash
virtualenv --no-site-packages venv
source venv/bin/activate
pip install -r requirements.txt
python -m ipykernel install --user --name venv --display-name  venv_a1chemy