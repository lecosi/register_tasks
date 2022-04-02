# Notebook project

## Installation

- Create a virtual environment (pyenv for example)
- Use Python 3.8+
- Install and Config postgres db
- Create database (exist a example in .envrc file)
- Config your database in .envrc file
- install requirements `pip install -r notebook/requirements/common.txt`
- Run server `python notebook/manage.py runserver 0.0.0.0:8000`


### Tests
- Install requirements `pip install -r notebook/requirements/test.txt`
- Run test `pytest -x` or `pytest -vv`

### Documentation 

- Postman `notebook.postman_collection.json` file 
- Apiary `https://notebook3.docs.apiary.io/#`