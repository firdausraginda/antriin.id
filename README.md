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

### Gunicorn
Install gunicorn
```sh
pip3 install gunicorn
```

Run this command (inside virtual env)
```sh
gunicorn -w 4 --reload -b 0.0.0.0:8089 'src:create_app()'
```

### Config File

* `.flaskenv` file
needed when using sqlite to store data & run via `flask run` local
```
export FLASK_ENV=development
export FLASK_APP=src
export SQLALCHEMY_DB_URI=sqlite:///antriin.db
```

* `.env` file
this is confidential file, don't need push to git or dockerhub repo
```
export SECRET_KEY="dev"
```

* `database.ini`
  * create `database.ini` file
  * adjust value of `database.ini` file with the `environment` value in `docker-compose.yaml`
  * if running flask & postgres using docker, the DB `host:port` can use DB service name in `docker-compose.yaml`
```
[postgresql]
host=postgres_db
database=antriin-db
username=super_admin
password=password
```

### Swagger

* [flasgger](https://github.com/flasgger/flasgger)
  * refer these docs to set `swagger.py`:
    * [initializing flasgger with default data](https://github.com/flasgger/flasgger#initializing-flasgger-with-default-data)
    * [custom default configurations](https://github.com/flasgger/flasgger#customize-default-configurations)
* refer [here](https://github.com/flasgger/flasgger#using-external-yaml-files) to define API docs in yaml file
* refer [here](https://swagger.io/docs/specification/2-0/authentication/) to define authorization
* swagger localhost: `http://127.0.0.1:5000/api/docs`

Install flasgger for better documentation
```sh
pip3 install -U setuptools
pip3 install flasgger
```

### Docker

#### Docker using `Dockerfile`

Docker image `firdausraginda/antriin_id:latest` initially created from this `Dockerfile`
```sh
FROM python:latest

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy scripts to folder
COPY . /app

# start the server
CMD gunicorn 'src:create_app()' -w 4 -b 0.0.0.0:8089 --reload
```

Build docker image
```sh
docker build -t antriin-id .
```

Create and run container
```sh
docker run -d -p 8089:8089 --name antriin-id-app antriin-id
```

Push image to dockerhub repo
```sh
docker tag antriin-id:latest firdausraginda/antriin-id:latest
docker push firdausraginda/antriin-id:latest
```

#### Docker using `docker-compose.yaml`

Create `docker-compose.yaml` file

Run docker compose
```sh
docker-compose up -d
```

Stop & remove docker container
```sh
docker-compose down
```

## Note

### [Application Factory](https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/)
Instead of creating a Flask instance globally, better to create it inside a function. This function is known as the application factory. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.