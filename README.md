# 🤝 learning-together<br>
>Support finding pair-programming partner.<br>

## 🛢 Motivation 
Help people to find a partner to do pair-programming. 

This app will: 

   - Support finding a partner for pair-programming. 
   - Support you to offer your free time for doing pair-programming. 

## 🔧 Tech & tools

- Python3
- Flask
- Postgres
- Docker(option)

## 🏍 Getting Started 
Before running any scripts, you'll need additional setups. After 2 steps, you should run the next command. 
```python

pip install -r requirements.txt
python main.py

```
Steps: 

   1. Add `.env` then put necessary values. You can fined a sample at `.env.example`

   2. Make a virtual environment<br>

      - Linux and Apple users
      
         1. Type: `[test@localhost ~]$ python3 -m venv <name>`
         2. Enter the virtual environment: `source <name>/bin/activate`

      - Windows users
      
         1. Type: `>virtualenv .<name>`
         2. Enter the virtual environment: `><name>\Scripts\activate`

      To leave the virtual environment. `(<name>) [test@localhost ~]$ deactivate`

## 🧰 Options : Use Docker

1. Install Docker and VSCode extension: Remote development 

2. Press `><` button which you can find at the left-bottom of the VSCode panel.

3. Chose `Open Folder in Container` of pop-up panel.<br>

4. Click a button which labeled as `Open`
   - If it is succeeded, you can see `Dev Container:ltw remote` at the next to the `><` button.
   
   - You can see the image of the website from `http://localhost:8000`.

6. Enable Github in your devcontainer.

   - You need to execute few commands. You can find the commands at `/.devcontainer/commands.example`

   - To check the availability of Github, type `ssh -v git@github.com`. We expect that you can see your github account.

## 🔩 Tips : Initialize a database 

1. Execute the command `flask db init` under `/app`

2. Add code below to `database/migrations/env.py`
   ```
   # ! Import the database model under here
   from database.models.user import UserProfile
   from database.models.password import UserPassword
   from database.models.schedule_datetime import ScheduleDatetime
   ```
3. Execute `flask db migrate -m 'initial migration'` under `/app`

4. Execute `flask db upgrade'` under `/app`

   - You can check the database using command `docker exec -it <container name> /bin/sh`<br>
      ※ Not inside the devcontainer. Execute them at the outside.<br>
   - Accessing the Postgres CLI : `psql --username postgres`

## 🏜 How To Use

Search opened slot in `Search`, if you´d like you can book it. 
Also you can offer your free time in `Schedule` 

## Our team

This app is created by [matt185](https://github.com/matt185) and [miku0129](https://github.com/miku0129).
