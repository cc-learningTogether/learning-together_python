# learning-together_python

### Welcome! [Here](https://learning-together.fly.dev/) is our website!!  

## How to start 

Prerequisite - Python3 

1. `git clone` this project. 

2. Create your own virtual environment. `[test@localhost ~]$ python3 -m venv .<name>` 

3. Enter the virtual environment. `source .<name>/bin/activate`

4. Install packages. `pip install -r requirements.txt`

5. You can test that the application works.Run this command on your terminal within the root directory to perform this test: `python app.py`

6. To leave the virtual environment. `(.<name>) [test@localhost ~]$ deactivate`

7. When you ready to share your change, push `development` branch in Github. 

## GitHub Container Registry 

#### Download Docker image from [here](https://github.com/users/miku0129/packages/container/package/learning-together_docker%2Flearning-together)

The command to run the image 
```
docker run -p <your port number>:8080 -d ghcr.io/miku0129/learning-together_docker/learning-together
```

