# Catalog restful api

## Installation

### Clone this project
`git clone https://github.com/ntt261298/Catalog-Restful-Flask-Api.git` 

### Create a virtual environment
`virtualenv env`
### Activate virtual env
`source env/bin/activate`

### Install requirements
`pip install -r requirements.txt`

### Choose environment
```
export ENV=development # for dev environment (default)
export ENV=production # for pro environment
export ENV=testing # for test environment
```
### Run Flask api
`python run.py`

### Run Test Unit
`python -m unittest discover`

### Migrate SQLAlchemy Database
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```