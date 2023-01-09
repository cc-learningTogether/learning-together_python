import os

from dotenv import load_dotenv

from app import create_app

from routes.router import initialize_routes

from utils.models.auth_manager import create_admin

# load_dotenv make possible to use a .env file for store the environment variable
load_dotenv()

# create the application
app = create_app()

with app.app_context():
    create_admin()

# initialize the router

initialize_routes(app)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
