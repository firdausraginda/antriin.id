# ANTRIIN.ID

## Dependencies

### Pip Freeze & Pip Install

* pip freeze
```sh
pip3 freeze > requirements.txt
```

* install from `requirements.txt`
```sh
pip3 install -r requirements.txt
```

### Virtual Env

* install virtual env
```sh
pip3 install virtualenv
```

* create virtual env
```sh
python3 -m venv vir-env
```

* activate virtual env
```sh
source vir-env/bin/activate
```

### Flask

* install flask
```sh
pip3 install flask
```

* run flask application
```sh
flask run
```

* install [python-dotenv](https://pypi.org/project/python-dotenv/) to utilize `.flaskenv`
```sh
pip3 install python-dotenv
```

* install [Flask SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#installation) to setup database
```sh
pip3 install Flask-SQLAlchemy
```

* install [Flask HTTP-Auth](https://flask-httpauth.readthedocs.io/en/latest/)
```sh
pip3 install Flask-HTTPAuth
```

### Config File

* `.env` file
```
export SECRET_KEY="dev"
```

### Other Dependencies

* install flasgger for better documentation
```sh
pip3 install -U setuptools
```

```sh
pip3 install flasgger
```
refer [here](https://swagger.io/specification/v2) to set `swagger.py`


## Note

### [Application Factory](https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/)
Instead of creating a Flask instance globally, better to create it inside a function. This function is known as the application factory. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.