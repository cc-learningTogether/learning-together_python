# learning-together_python

### Welcome! [Here](https://learning-together.fly.dev/) is our website!!  

## Tech 

- Python (Flask, jinjya, venv)
- Postgres
- Docker 
- Fly.io

## How to start 

Prerequisite - Installing Python, docker and docker-compose

1. `git clone` this project. 

2. Create then enter virtual environment. <br>

  * __Linux and Apple users__
    * 1. Type `[test@localhost ~]$ python3 -m venv .<name>` 
    * 2. Enter the virtual environment. `source .<name>/bin/activate`
  
  * __Windows users__
    * 1. Type `>virtualenv .<name>` 
    * 2. Enter the virtual environment. `>.<name>\Scripts\activate`
  
3. Install packages. `pip install -r requirements.txt`

4. You can test that the application works.Run this command on your terminal within the root directory to perform this test: `python app.py`

5. To leave the virtual environment. `(.<name>) [test@localhost ~]$ deactivate`

6. When you ready to share your change, push `development` branch in Github. 

## If you start docker container

- start Docker container: `docker compose up` 
  - [If you change Dockerfile or docker-compose.yml](https://qiita.com/nasuB7373/items/523f1392d87dffb5521d): `docker compose up -d --build`
  
- stop & remove Docker container: `docker compose stop`


## GitHub Container Registry 

#### Download Docker image from [here](https://github.com/users/miku0129/packages/container/package/learning-together_docker%2Flearning-together)

The command to run the image 
```
docker run -p <your port number>:8080 -d ghcr.io/miku0129/learning-together_docker/learning-together
```

