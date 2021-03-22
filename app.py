import os
from flask import Flask

from warnings import filterwarnings
filterwarnings('ignore')


cwd = os.getcwd()
DESTINATION_FOLDER= os.path.join(cwd, 'downloads')
print(DESTINATION_FOLDER)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'recogsign'
app.config['DESTINATION_FOLDER'] = DESTINATION_FOLDER

from routes import *

if __name__=='__main__':
    app.run(debug=True)