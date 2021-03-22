import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from warnings import filterwarnings
filterwarnings('ignore')

cwd = os.getcwd()
print(f'Current Working Directory: {cwd}')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'recogsign'
db = SQLAlchemy(app)

from routes import *

if __name__=='__main__':
    app.run(debug=True)