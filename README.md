# learning-together<br>
<img src="https://i.ibb.co/9njFRxz/photo-1546410531-bb4caa6b424d.jpg" width="500"><br>
© Photo by Tim Mossholde<br><br>
Welcome!! <br>
[Here](https://learning-together.fly.dev/) is our website!!  

## What is learning-together ? 📚🤓

learning-together is an app to support finding pair programming partner. <br>
Output your thought is the best way to brashup your skill. <br>
I hope it help you dive into programming world ! 

## Tech 🛠️

- Python (Flask, jinjya, venv)
- Postgres
- Docker 
- VSCode(It must be able to access to your Github repository)
- Remote development(vscode extention)
- Fly.io
  
## How to start 🛴

Prerequisite - Install Python, docker and docker-compose to your machine. Install Remote Dvelopment to your VSCode. 

1. `git clone` this project. 

2. Add `.env` then write your settings. You can fined a sample at `.env.example`

3. Press `><` button which you can find at the left-bottom of the VSCode panel. 

4. Chose `Open Folder in Container` of pop-up panel.<br>
    ※ If you've created container & image already, chose `Reopen in Container`.<br>

5. Click a button which labeled as `Open` 
   - If it is succeeded, you can see `Dev Container:ltw remote` at the next to the `><` button.<br>
      You can see the image of the website from `http://localhost:8000`.
   
6. Enable Github in your devcontainer. 
   - You need to excute few commands. You can find the commands at `/.devcontainer/commands.example`
   
   - To check the abairablity of Github, type `ssh -v git@github.com`. We expect that you can see your github account.

6. Initialize the database 
   1. Excute the command `flask db init` under `/app`. 
   2. Add code below to `database/migrations/env.py`
      ```
      # ! Import the database model under here
      from database.models.user import UserProfile
      from database.models.password import UserPassword
      from database.models.schedule_datetime import ScheduleDatetime
      ```
   3. Excute `flask db migrate -m 'initial migration'` under `/app`. 
   4. Excute `flask db upgrade'` under `/app`. 
   - You can check the database using command `docker exec -it <container name> /bin/sh` 
      - ※ Not inside the devcontainer. Excute them at the outside.  
   - Accessing the Postgres CLI : `psql --username postgres`
   - Quit the psql: `\q` 

## DEV 🏍️

1. Make virtual environment. <br>

  * __Linux and Apple users__
    * 1. Type `[test@localhost ~]$ python3 -m venv <name>` 
    * 2. Enter the virtual environment. `source <name>/bin/activate`
  
  ~~* __Windows users__~~
    ~~* 1. Type `>virtualenv .<name>`~~ 
    ~~* 2. Enter the virtual environment. `><name>\Scripts\activate`~~
  
2. Install packages. Excute: `pip install -r requirements.txt`
  - If you add package, add that informatiEon to requirementx.txt: `pip freeze > requirements.txt`

4. You can test that the application works.Run this command on your terminal within the root directory to perform this test: `python main.py`

5. To leave the virtual environment. `(<name>) [test@localhost ~]$ deactivate`

6. When you ready to update code, push to the `development` branch in Github. 


## Our team 

This app is created by [matt185](https://github.com/matt185) and [miku0129](https://github.com/miku0129). 

