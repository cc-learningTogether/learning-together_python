# learning-together_python

### Welcome! [Here](https://learning-together.fly.dev/) is our website!!  

## Tech 

- Python (Flask, jinjya, venv)
- Postgres
- Docker 
- Fly.io

## How to start 

Prerequisite - Python3 

1. `git clone` this project. 

2. Create your own virtual environment. `[test@localhost ~]$ python3 -m venv .<name>` 

3. Enter the virtual environment. `source .<name>/bin/activate`

4. Install packages. `pip install -r requirements.txt`

5. You can test that the application works.Run this command on your terminal within the root directory to perform this test: `python app.py`

6. To leave the virtual environment. `(.<name>) [test@localhost ~]$ deactivate`

7. When you ready to share your change, push `development` branch in Github. 

## How to start docker container 

1. Check containers `docker ps -a`

2. Create a new container, start the container  `docker run --name <prefer container name> -p <your prefer port number>:8080 -d <docker image name>` <br>
  If you've already created a container , you can start the container with `docker start <container name>`<br>
  Also you can stop the container `docker stop <container name>`
  
3. If you'd like to have a look inside the container, `docker container exec -it <container name> bash`
  if you'd like to exit, type `exit` in the terminal. 

## How to get a image from GitHub Container Registry 

#### Download Docker image from [here](https://github.com/users/miku0129/packages/container/package/learning-together_docker%2Flearning-together)

The command to run the image 
```
docker run -p <your port number>:8080 -d ghcr.io/miku0129/learning-together_docker/learning-together
```

