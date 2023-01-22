FROM python:latest

# set the working directory
WORKDIR /app

# install dependencies
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# copy scripts to folder
COPY . /app

# start the server
ENTRYPOINT ["gunicorn", "-w", "4", "--reload", "-b", "0.0.0.0:8089","src:create_app()"]