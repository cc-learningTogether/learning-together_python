from flask import Flask
from dotenv import load_dotenv
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager
from test_data_folder.user_data import users
import os


def create_app():
    # initialize the env variable
    load_dotenv()

    app = Flask(__name__)
    # set Secret key (required from wtForms
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    # add bootstrap version 5 to the application
    bootstrap = Bootstrap5(app)

    login_manager = LoginManager()
    login_manager.init_app(app=app)

    @login_manager.user_loader
    def load_user(user_id):
        user = [user for user in users if user["user_id"] == int(user_id)]
        return user[0]

    if __name__ == "__main__":
        port = int(os.environ.get('PORT', 8080))
        app.run(debug=True, host='0.0.0.0', port=port)

    return app
