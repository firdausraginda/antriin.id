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

* `.flaskenv` file
```
export FLASK_ENV=development
export FLASK_APP=src
export SQLALCHEMY_DB_URI=sqlite:///antriin.db
```

## database.ini
create `database.ini` file
adjust value with the `environment` value in `docker-compose.yaml`
```
[postgresql]
host=localhost
port=8088
database=antriin-db
username=super_admin
password=password
```

### Swagger

* [flasgger](https://github.com/flasgger/flasgger)
refer to these docs to set `swagger.py`:
    * [initializing flasgger with default data](https://github.com/flasgger/flasgger#initializing-flasgger-with-default-data)
    * [custom default configurations](https://github.com/flasgger/flasgger#customize-default-configurations)

refer [here](https://github.com/flasgger/flasgger#using-external-yaml-files) to define API docs in yaml file

refer [here](https://swagger.io/docs/specification/2-0/authentication/) to define authorization

swagger localhost: `http://127.0.0.1:5000/api/docs`

install flasgger for better documentation
```sh
pip3 install -U setuptools
```

```sh
pip3 install flasgger
```

### Gunicorn
Run this command **outside the virtual env**
```sh
gunicorn -w 4 --reload -b 0.0.0.0:8089 'src:create_app()'
```

### Docker
Build docker image
```sh
docker build -t antriin_id .
```

Create and run container
```sh
docker run -d -p 8089:8089 antriin_id
```

Run docker compose
```sh
docker-compose up -d
```

Push image to docker repo
```sh
docker tag <local-image>:<tagname> <new-repo>:<tagname>
docker push <new-repo>:<tagname>
```

#### Run postgres docker (without docker-compose)
Pull postgresql image
```sh
docker pull postgres
```

List down docker network
```sh
docker network ls
```

Create docker network
```sh
docker network create <network-name>
```

Create container
```sh
docker run -d \
-p 8088:5432 \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_USER=super_admin \
-e POSTGRES_DB=antriin-db \
--name antriin-postgres \
--net antriinid-network \
postgres
```

## Note

### [Application Factory](https://flask.palletsprojects.com/en/2.1.x/tutorial/factory/)
Instead of creating a Flask instance globally, better to create it inside a function. This function is known as the application factory. Any configuration, registration, and other setup the application needs will happen inside the function, then the application will be returned.