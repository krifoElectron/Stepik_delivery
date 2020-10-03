from flask import Flask
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.views import *

if __name__ == '__main__':
    app.run(debug=True)
