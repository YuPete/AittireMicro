FROM python:3.10-slim-bullseye 
#base image


RUN apt-get update \
#retrieves latest list of available packages so when you download later, 
#it is most recent version
  &&apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential \
  # -y automatically answers yes to prompts, --no-install-rec & --no-install-suggests 
  # prevent installing recommended/suggested packages
  # only installs 1.build-essential (package important for software building)
  # 2. default-libmysqlclient-dev: Development files for MySQL client 
  && pip install --no-cache-dir --upgrade pip
  #installs pip while not caching packages it downloads (smaller image size)

WORKDIR /app
#sets working directory to "/app";" any later commands run in this directory 

COPY ./requirements.txt /app
#copies requirements.txt from host machine to "/app" directory in Docker build 

#remove /app!!!!!!
RUN pip install --no-cache-dir --requirement /app/requirements.txt 
#pip installs content of requirements.txt

COPY . /app
#copies content of CWD of host to /app in container (first param always on host)
#try COPY . . 

EXPOSE 8080
#documents that Docker listens on port 5000 

CMD ["python3", "server.py"]
#run "python3 server.py" command in docker container





  