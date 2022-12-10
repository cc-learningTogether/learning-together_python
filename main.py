import os

from dotenv import load_dotenv

from app import create_app

from routes.home import home_route
from routes.signup import signup_route
from routes.signin import signin_route
from routes.logout import logout_route
from routes.forgot_password import forgot_password_route
from routes.change_password import change_psw_route
from routes.settings import settings_route

# load_dotenv make possible to use a .env file for store the environment variable
load_dotenv()

# create the application
app = create_app()

# Register the blueprint (routes)
app.register_blueprint(home_route)

app.register_blueprint(signup_route)

app.register_blueprint(signin_route)

app.register_blueprint(logout_route)

app.register_blueprint(forgot_password_route)

app.register_blueprint(change_psw_route)

app.register_blueprint(settings_route)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
