from flask import Flask, render_template
from flask_bootstrap import Bootstrap4
import os

app = Flask(__name__)
bootstrap = Bootstrap4(app)
SITE_NAME = "Learning Together"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    return render_template('register.html', name=SITE_NAME)


@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html', name=SITE_NAME)


@app.route('/logout', methods=["GET", "POST"])
def logout():
    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
