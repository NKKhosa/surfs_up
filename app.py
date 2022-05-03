# import dependencies
from flask import Flask 

# create a new Flask instance
app = Flask(__name__)

# define the root
@app.route('/')

# create a function for the code you want in that route
def hello_world():
    return 'Hello world.'

