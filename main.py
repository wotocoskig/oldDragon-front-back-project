from flask import Flask
from flask import render_template
#Flask sqlalchemy tabelas para banco de dados
#flask wtf forms formularios

app = Flask(__name__)

from routes import *

if __name__ == "__main__":
    app.run()
    