from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from datetime import datetime
import os

app = Flask(__name__)
# Initialize Bootstrap5
bootstrap = Bootstrap5(app)

year = datetime.now().year


@app.route('/')
def home():
    return render_template('index.html', year=year)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
