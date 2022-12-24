from routes.home import home_route
from routes.signup import signup_route
from routes.signin import signin_route
from routes.logout import logout_route
from routes.forgot_password import forgot_password_route
from routes.change_password import change_psw_route
from routes.settings import settings_route
from routes.scheduling_datetime import scheduling_datetime_route


def initialize_routes(app):
    app.register_blueprint(home_route)

    app.register_blueprint(signup_route)

    app.register_blueprint(signin_route)

    app.register_blueprint(logout_route)

    app.register_blueprint(forgot_password_route)

    app.register_blueprint(change_psw_route)

    app.register_blueprint(settings_route)

    app.register_blueprint(scheduling_datetime_route)
